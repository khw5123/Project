# -*- coding: utf-8 -*-
import os
import json
import tarfile
import win32api
import win32con
import six.moves.urllib as urllib
from tqdm import tqdm
from time import gmtime, strftime
from PIL import Image, ImageGrab
from threading import Thread
import cv2
import numpy as np
import tensorflow as tf

try:
    from moviepy.editor import VideoFileClip
except:
    import imageio
    imageio.plugins.ffmpeg.download()
    from moviepy.editor import VideoFileClip

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

class DetectionObj(object):
    def __init__(self, model=1, thresh=0.25):
        self.CURRENT_PATH = os.getcwd() # 현재 경로
        self.MODELS = [
            'ssd_mobilenet_v1_coco_11_06_2017', 
            'ssd_inception_v2_coco_11_06_2017', 
            'rfcn_resnet101_coco_11_06_2017', 
            'faster_rcnn_resnet101_coco_11_06_2017', 
            'faster_rcnn_inception_resnet_v2_atrous_coco_11_06_2017'
        ] # 미리 학습된 텐서플로 탐지 모델 Zoo
        self.THRESHOLD = thresh # 탐지 신뢰도 최솟값
        if model > 0 and model <= len(self.MODELS):
            self.MODEL_NAME = self.MODELS[model - 1]
        else:
            print('Model not available, reverted to default', self.MODELS[0])
            self.MODEL_NAME = self.MODELS[0]
        self.CKPT_FILE = os.path.join(self.CURRENT_PATH, 'object_detection', self.MODEL_NAME, 'frozen_inference_graph.pb') # 미리 학습된 텐서플로 frozen 모델 파일
        try:
            self.DETECTION_GRAPH = self.load_frozen_model()
        except:
            print ('Couldn\'t find', self.MODEL_NAME)
            self.download_frozen_model()
            self.DETECTION_GRAPH = self.load_frozen_model()
        self.NUM_CLASSES = 90 # MS COCO 데이터셋에서 인식 가능한 범주 수
        path_to_labels = os.path.join(self.CURRENT_PATH, 'object_detection', 'data', 'mscoco_label_map.pbtxt')
        label_mapping = label_map_util.load_labelmap(path_to_labels)
        extracted_categories = label_map_util.convert_label_map_to_categories(label_mapping, max_num_classes=self.NUM_CLASSES, use_display_name=True)
        self.LABELS = {item['id']: item['name'] for item in extracted_categories}
        self.CATEGORY_INDEX = label_map_util.create_category_index(extracted_categories)
        self.TF_SESSION = tf.Session(graph=self.DETECTION_GRAPH) # 텐서플로 세션 실행
    
    def load_frozen_model(self): # 미리 학습된 텐서플로 frozen 모델 로드 메서드
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.CKPT_FILE, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return detection_graph
    
    def download_frozen_model(self): # 미리 학습된 텐서플로 frozen 모델 다운로드 메서드
        def my_hook(t):
            last_b = [0]
            def inner(b=1, bsize=1, tsize=None):
                if tsize is not None:
                    t.total = tsize
                t.update((b - last_b[0]) * bsize)
                last_b[0] = b
            return inner
        model_filename = self.MODEL_NAME + '.tar.gz'
        download_url = 'http://download.tensorflow.org/models/object_detection/'
        opener = urllib.request.URLopener()
        print('Downloading ...')
        with tqdm() as t:
            opener.retrieve(download_url + model_filename, model_filename, reporthook=my_hook(t))
        print ('Extracting ...')
        tar_file = tarfile.open(model_filename)
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)
            if 'frozen_inference_graph.pb' in file_name:
                tar_file.extract(file, os.path.join(self.CURRENT_PATH, 'object_detection'))
    
    def load_image_from_disk(self, image_path): # 이미지 파일 오픈 메서드
        return Image.open(image_path)
    
    def load_image_into_numpy_array(self, image): # 이미지 파일 넘파이 배열 변환 메서드
        try:
            (im_width, im_height) = image.size
            return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
        except:
            return image
    
    def detect(self, images, annotate_on_image=True): # 객체 탐지 및 윤곽 추가 메서드
        if type(images) is not list:
            images = [images]
        results = list()
        for image in images:
            image_np = self.load_image_into_numpy_array(image) # 이미지 배열
            image_np_expanded = np.expand_dims(image_np, axis=0) # 차원 확장(이미지 개수(1) x 높이 x 너비 x 깊이(3))
            image_tensor = self.DETECTION_GRAPH.get_tensor_by_name('image_tensor:0')
            boxes = self.DETECTION_GRAPH.get_tensor_by_name('detection_boxes:0')
            scores = self.DETECTION_GRAPH.get_tensor_by_name('detection_scores:0')
            classes = self.DETECTION_GRAPH.get_tensor_by_name('detection_classes:0')
            num_detections = self.DETECTION_GRAPH.get_tensor_by_name('num_detections:0')
            (boxes, scores, classes, num_detections) = self.TF_SESSION.run([boxes, scores, classes, num_detections], feed_dict={image_tensor: image_np_expanded}) # 탐지
            if annotate_on_image: # 탐지된 객체의 윤곽 출력으로 설정했을 경우
                new_image = self.detection_on_image(image_np, boxes, scores, classes) # 기존 이미지에 탐지된 객체의 윤곽 추가
                results.append((new_image, boxes, scores, classes, num_detections))
            else:
                results.append((image_np, boxes, scores, classes, num_detections))
        return results
    
    def detection_on_image(self, image_np, boxes, scores, classes): # 탐지된 객체의 윤곽이 추가된 이미지 반환 메서드
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np, 
            np.squeeze(boxes), 
            np.squeeze(classes).astype(np.int32), 
            np.squeeze(scores), 
            self.CATEGORY_INDEX, 
            use_normalized_coordinates=True, 
            line_thickness=8
        )
        return image_np
    
    def visualize_image(self, image_np, image_size=(400, 300), latency=3, bluish_correction=True): # 탐지된 이미지 출력 메서드
        height, width, depth = image_np.shape
        reshaper = height / float(image_size[0])
        width = int(width / reshaper)
        height = int(height / reshaper)
        id_img = 'preview_' + str(np.sum(image_np))
        cv2.startWindowThread()
        cv2.namedWindow(id_img, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(id_img, width, height)
        if bluish_correction:
            RGB_img = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            cv2.imshow(id_img, RGB_img)
        else:
            cv2.imshow(id_img, image_np)
        cv2.waitKey(latency*1000)
    
    def serialize_annotations(self, boxes, scores, classes, filename='data.json'): # json 파일에 탐지 범주, 윤곽 위치, 탐지 신뢰도 기록 메서드
        threshold = self.THRESHOLD
        valid = [position for position, score in enumerate(scores[0]) if score > threshold]
        if len(valid) > 0:
            valid_scores = scores[0][valid].tolist()
            valid_boxes  = boxes[0][valid].tolist()
            valid_class = [self.LABELS[int(a_class)] for a_class in classes[0][valid]]
            with open(filename, 'w') as outfile:
                json_data = json.dumps({'classes': valid_class, 'boxes':valid_boxes, 'scores': valid_scores})
                json.dump(json_data, outfile)
    
    def get_time(self):
        return strftime('%Y-%m-%d_%Hh%Mm%Ss', gmtime())
    
    def annotate_photogram(self, photogram):
        new_photogram, boxes, scores, classes, num_detections = self.detect(photogram)[0]
        return new_photogram
    
    def file_pipeline(self, images, visualize=True): # 이미지 파일에서 객체 탐지 및 처리 메서드
        if type(images) is not list:
            images = [images]
        for filename in images:
            single_image = self.load_image_from_disk(filename)
            for new_image, boxes, scores, classes, num_detections in self.detect(single_image):
                self.serialize_annotations(boxes, scores, classes, filename=filename + '.json')
                if visualize:
                    self.visualize_image(new_image)
    
    def video_pipeline(self, video, audio=False): # 동영상 파일에서 객체 탐지 및 처리 메서드
        clip = VideoFileClip(video)
        new_video = video.split('/')
        new_video[-1] = 'annotated_' + new_video[-1]
        new_video = '/'.join(new_video)
        video_annotation = clip.fl_image(self.annotate_photogram)
        video_annotation.write_videofile(new_video, audio=audio)
    
    def capture_webcam(self):
        def get_image(device):
            retval, im = device.read()
            return im
        camera_port = 0
        ramp_frames = 30
        camera = cv2.VideoCapture(camera_port)
        for i in range(ramp_frames):
            _ = get_image(camera)
        camera_capture = get_image(camera)
        del (camera)
        return camera_capture
    
    def webcam_pipeline(self): # 웹캠에서 객체 탐지 및 처리 메서드
        webcam_image = self.capture_webcam()
        filename = 'webcam_' + self.get_time()
        saving_path = os.path.join(self.CURRENT_PATH, filename + '.jpg')
        cv2.imwrite(saving_path, webcam_image)
        new_image, boxes, scores, classes, num_detections = self.detect(webcam_image)[0]
        json_obj = {'classes': classes, 'boxes': boxes, 'scores': scores}
        self.serialize_annotations(boxes, scores, classes, filename=filename+'.json')
        self.visualize_image(new_image, bluish_correction=False)

def resize(image, new_width=None, new_height=None):
    height, width, depth = image.shape
    if new_width:
        new_height = int((new_width / float(width)) * height)
    elif new_height:
        new_width = int((new_height / float(height)) * width)
    else:
        return image
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

class WebcamStream:
    def __init__(self, model):
        self.detection = DetectionObj(model=model)
        self.stream = cv2.VideoCapture(0)
        _, self.frame = self.stream.read()
        self.stop = False
        Thread(target=self.refresh, args=()).start()
    
    def refresh(self):
        while True:
            if self.stop:
                return
            _, self.frame = self.stream.read()
    
    def get(self):
        return self.detection.annotate_photogram(self.frame)
    
    def halt(self):
        self.stop = True

class WindowStream:
    def __init__(self, model):
        self.detection = DetectionObj(model=model)
        self.screenWidth = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) # 윈도우 가로 크기
        self.screenHeight = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) # 윈도우 세로 크기
        self.currentFrame = ImageGrab.grab(bbox=(0, 0, self.screenWidth, self.screenHeight)) # 현재 윈도우 프레임
        self.frame = np.array(self.currentFrame) # 현재 프레임
        self.stop = False # 중지 유무
        Thread(target=self.refresh, args=()).start()
    
    def refresh(self):
        while True:
            if self.stop:
                return
            self.currentFrame = ImageGrab.grab(bbox=(0, 0, self.screenWidth, self.screenHeight)) # 현재 윈도우 프레임
            self.frame = np.array(self.currentFrame) # 현재 프레임
    
    def get(self):
        return self.detection.annotate_photogram(self.frame)
    
    def halt(self):
        self.stop = True

def main():
    try:
        sel = input('\n1. Image\n2. Video\n3. Webcam\n4. Windows\nSelect : ')
        model = int(input('\n[Model]\n1. ssd_mobilenet_v1_coco_11_06_2017\n2. ssd_inception_v2_coco_11_06_201\n3. rfcn_resnet101_coco_11_06_2017\n4. faster_rcnn_resnet101_coco_11_06_2017\n5. faster_rcnn_inception_resnet_v2_atrous_coco_11_06_2017\nSelect : '))
        if sel == '1':
            detection = DetectionObj(model=model)
            images = []
            while True:
                image = input('Input image file : ')
                images.append(image)
            detection.file_pipeline(images)
            return
        elif sel == '2':
            detection = DetectionObj(model=model)
            video = input('Input video file : ')
            detection.video_pipeline(video=video, audio=False)
            # detection.webcam_pipeline()
            return
        elif sel == '3':
            stream = WebcamStream(model=model)
        elif sel == '4':
            stream = WindowStream(model=model)
        size = input('Do you want to set the size?(Y/N): ')
        width, height = None, None
        if size.lower() == 'y' or size.lower() == 'yes':
            width = int(input('Input width : '))
            height = int(input('Input height : '))
        while True:
            if width:
                frame = resize(stream.get(), new_width=width, new_height=height)
            else:
                frame = stream.get()
            cv2.imshow('Show', frame)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                stream.halt()
                break
    except Exception as e:
        print('[-]', e)

if __name__ == '__main__':
    main()