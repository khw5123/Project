# -*- coding: utf-8 -*-
import math
import gzip
import warnings
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from scipy.misc import imresize
from random import shuffle
from distutils.version import LooseVersion

class Dataset(object):
    def __init__(self, data, labels=None, width=28, height=28, max_value=255, channels=3):
        self.IMAGE_WIDTH = width # 변환될 이미지 가로 크기
        self.IMAGE_HEIGHT = height # 변환될 이미지 세로 크기
        self.IMAGE_MAX_VALUE = float(max_value) # 이미지 컬러 최댓값
        self.CHANNELS = channels # 채널 수
        self.shape = len(data), self.IMAGE_WIDTH, self.IMAGE_HEIGHT, self.CHANNELS
        if self.CHANNELS == 3:
            self.image_mode = 'RGB'
            self.cmap = None
        elif self.CHANNELS == 1:
            self.image_mode = 'L'
            self.cmap = 'gray'
        if data.shape[1] != self.IMAGE_HEIGHT or data.shape[2] != self.IMAGE_WIDTH: # 이미지가 설정한 변환될 이미지 크기와 다를 경우
            data = self.image_resize(data, self.IMAGE_HEIGHT, self.IMAGE_WIDTH) # 이미지 리사이징
        index = list(range(len(data)))
        shuffle(index) # 인덱스 셔플
        self.data = data[index] # 이미지 셔플해서 저장
        if len(labels) > 0: # 레이블이 있을 경우
            self.labels = labels[index] # 레이블 셔플해서 저장
            self.classes = np.unique(labels) # 레이블 중복 제거해서 저장
            one_hot = dict()
            no_classes = len(self.classes)
            for j, i in enumerate(self.classes): # 클래스(분류)를 이용해서 원-핫 인코딩
                one_hot[i] = np.zeros(no_classes)
                one_hot[i][j] = 1.0
            self.one_hot = one_hot # 원-핫 인코딩 벡터
        else: # 레이블이 없을 경우
            self.labels = None
            self.classes = None
            self.one_hot = None
    
    def image_resize(self, dataset, newHeight, newWidth): # 이미지 리사이징 메서드
        channels = dataset.shape[3]
        images_resized = np.zeros([0, newHeight, newWidth, channels], dtype=np.uint8)
        for image in range(dataset.shape[0]):
            if channels == 1:
                temp = imresize(dataset[image][:, :, 0], [newHeight, newWidth], 'nearest')
                temp = np.expand_dims(temp, axis=2)
            else:
                temp = imresize(dataset[image], [newHeight, newWidth], 'nearest')
            images_resized = np.append(images_resized, np.expand_dims(temp, axis=0), axis=0)
        return images_resized
    
    def get_batches(self, batch_size): # 배치 반환 메서드
        current_index = 0
        while current_index < self.shape[0]:
            if current_index + batch_size > self.shape[0]: # 패딩
                batch_size = self.shape[0] - current_index
            data_batch = self.data[current_index:current_index + batch_size]
            if len(self.labels) > 0:
                y_batch = np.array([self.one_hot[k] for k in self.labels[current_index:current_index + batch_size]])
            else:
                y_batch = np.array([])
            current_index += batch_size
            yield (data_batch / self.IMAGE_MAX_VALUE) - 0.5, y_batch # 이미지를 -0.5 ~ 0.5 사이의 값으로 변환해서 원-핫 인코딩된 레이블과 함께 반환

class CGan(object):
    def __init__(self, dataset, epochs=1, batch_size=32, z_dim=96, generator_name='generator', alpha=0.2, smooth=0.1, learning_rate=0.001, beta1=0.35):
        self.check_system() # 텐서플로 버전 및 GPU 장치 체크
        self.generator_name = generator_name # 학습 기록 저장 디렉터리
        self.dataset = dataset
        self.cmap = self.dataset.cmap
        self.image_mode = self.dataset.image_mode
        self.epochs = epochs
        self.batch_size = batch_size
        self.z_dim = z_dim # 생성기에서 사용할 랜덤 입력의 차원
        self.alpha = alpha
        self.smooth = smooth # 평활값
        self.learning_rate = learning_rate # 최적화 학습율
        self.beta1 = beta1 # 최적화 지수 붕괴율
        self.g_vars = list() # 생성기 텐서플로 변수 리스트
        self.trained = False # 학습 기록 존재 여부
    
    def check_system(self): # 텐서플로 버전 및 GPU 장치 체크 메서드
        version = tf.__version__
        print('TensorFlow Version: %s' % version)
        assert LooseVersion(version) >= LooseVersion('1.2'), ('You are using %s, please use TensorFlow version 1.2 or newer.' % version)
        if not tf.test.gpu_device_name():
            warnings.warn('No GPU found installed on the system. It is advised to train your GAN using a GPU or on AWS')
        else:
            print('Default GPU Device: %s' % tf.test.gpu_device_name())
    
    def instantiate_inputs(self, image_width, image_height, image_channels, z_dim, classes): # 텐서플로 변수 생성 메서드
        inputs_real = tf.placeholder(tf.float32, (None, image_width, image_height, image_channels), name='input_real') # 실제 입력 이미지 텐서플로 변수
        inputs_z = tf.placeholder(tf.float32, (None, z_dim + classes), name='input_z') # 생성기에 의해 생성된 이미지 텐서플로 변수
        labels = tf.placeholder(tf.float32, (None, image_width, image_height, classes), name='labels') # 레이블 텐서플로 변수
        learning_rate = tf.placeholder(tf.float32, None) # 학습율 텐서플로 변수
        return inputs_real, inputs_z, labels, learning_rate
    
    def leaky_ReLU_activation(self, x, alpha=0.2): # ReLU 활성함수
        return tf.maximum(alpha * x, x)
    
    def dropout(self, x, keep_prob=0.9): # Dropout 메서드
        return tf.nn.dropout(x, keep_prob)
    
    def d_conv(self, x, filters, kernel_size, strides, padding='same', alpha=0.2, keep_prob=0.5, train=True): # CNN
        x = tf.layers.conv2d(x, filters, kernel_size, strides, padding, kernel_initializer=tf.contrib.layers.xavier_initializer()) # 합성곱 레이어
        x = tf.layers.batch_normalization(x, training=train) # 배치 정규화
        x = self.leaky_ReLU_activation(x, alpha) # ReLU 활성함수 적용
        x = self.dropout(x, keep_prob) # Dropout 적용
        return x
    
    def g_reshaping(self, x, shape, alpha=0.2, keep_prob=0.5, train=True): # 생성될 이미지 형상화 메서드
        x = tf.reshape(x, shape)
        x = tf.layers.batch_normalization(x, training=train)
        x = self.leaky_ReLU_activation(x, alpha)
        x = self.dropout(x, keep_prob)
        return x
    
    def g_conv_transpose(self, x, filters, kernel_size, strides, padding='same', alpha=0.2, keep_prob=0.5, train=True): # CNN 전치
        x = tf.layers.conv2d_transpose(x, filters, kernel_size, strides, padding) # CNN 전치
        x = tf.layers.batch_normalization(x, training=train)
        x = self.leaky_ReLU_activation(x, alpha)
        x = self.dropout(x, keep_prob)
        return x
    
    def discriminator(self, images, labels, reuse=False): # 분류기
        with tf.variable_scope('discriminator', reuse=reuse):
            x = tf.concat([images, labels], 3) # 입력 이미지와 레이블 결합
            x = self.d_conv(x, filters=32, kernel_size=5, strides=2, padding='same', alpha=0.2, keep_prob=0.5) # CNN(14 x 14 x 32)
            x = self.d_conv(x, filters=64, kernel_size=5, strides=2, padding='same', alpha=0.2, keep_prob=0.5) # CNN(7 x 7 x 64)
            x = self.d_conv(x, filters=128, kernel_size=5, strides=1, padding='same', alpha=0.2, keep_prob=0.5) # CNN(7 x 7 x 128)
            x = tf.reshape(x, (-1, 7 * 7 * 128))
            logits = tf.layers.dense(x, 1) # 완전 연결 레이어
            sigmoids = tf.sigmoid(logits)
            return sigmoids, logits
    
    def generator(self, z, out_channel_dim, is_train=True): # 생성기
        with tf.variable_scope('generator', reuse=(not is_train)):
            x = tf.layers.dense(z, 7 * 7 * 512) # 완전 연결 레이어
            x = self.g_reshaping(x, shape=(-1, 7, 7, 512), alpha=0.2, keep_prob=0.5, train=is_train) # 형상화
            x = self.g_conv_transpose(x, filters=256, kernel_size=5, strides=2, padding='same', alpha=0.2, keep_prob=0.5, train=is_train) # CNN 전치(7 x 7 x 128)
            x = self.g_conv_transpose(x, filters=128, kernel_size=5, strides=2, padding='same', alpha=0.2, keep_prob=0.5, train=is_train) # CNN 전치(14 x 14 x 64)
            logits = tf.layers.conv2d_transpose(x, filters=out_channel_dim, kernel_size=5, strides=1, padding='same') # CNN 전치(28 x 28 x 5)
            output = tf.tanh(logits)
            return output
    
    def loss(self, input_real, input_z, labels, out_channel_dim): # 오차 반환 메서드
        g_output = self.generator(input_z, out_channel_dim) # 생성기 출력(생성된 이미지)
        d_output_real, d_logits_real = self.discriminator(input_real, labels, reuse=False) # 실제 이미지 분류
        d_output_fake, d_logits_fake = self.discriminator(g_output, labels, reuse=True) # 생성된 이미지 분류
        real_input_labels = tf.ones_like(d_output_real) * (1 - self.smooth) # 실제 이미지 레이블
        d_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=d_logits_real, labels=real_input_labels)) # 실제 이미지 오차
        fake_input_labels = tf.zeros_like(d_output_fake) # 생성된 이미지 레이블
        d_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=d_logits_fake, labels=fake_input_labels)) # 생성된 이미지 오차
        d_loss = d_loss_real + d_loss_fake # 실제 이미지 오차와 생성된 이미지 오차의 합
        target_fake_input_labels = tf.ones_like(d_output_fake) # 생성된 이미지 레이블
        g_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=d_logits_fake, labels=target_fake_input_labels)) # 생성된 이미지 오차
        return d_loss, g_loss
    
    def rescale_images(self, image_array):
        new_array = image_array.copy().astype(float)
        min_value = new_array.min()
        range_value = new_array.max() - min_value
        new_array = ((new_array - min_value) / range_value) * 255
        return new_array.astype(np.uint8)
    
    def images_grid(self, images, n_cols):
        n_images, height, width, depth = images.shape
        n_rows = n_images // n_cols
        projected_images = n_rows * n_cols
        images = self.rescale_images(images)
        if projected_images < n_images:
            images = images[:projected_images]
        square_grid = images.reshape(n_rows, n_cols, height, width, depth)
        square_grid = square_grid.swapaxes(1, 2)
        if depth >= 3:
            return square_grid.reshape(height * n_rows, width * n_cols, depth)
        else:
            return square_grid.reshape(height * n_rows, width * n_cols)
    
    def plotting_images_grid(self, n_images, samples):
        n_cols = math.floor(math.sqrt(n_images))
        images_grid = self.images_grid(samples, n_cols)
        plt.imshow(images_grid, cmap=self.cmap)
        plt.show()
    
    def show_generator_output(self, sess, n_images, input_z, labels, out_channel_dim, image_mode):
        z_dim = input_z.get_shape().as_list()[-1]
        example_z = np.random.uniform(-1, 1, size=[n_images, z_dim - labels.shape[1]])
        example_z = np.concatenate((example_z, labels), axis=1)
        sample = sess.run(self.generator(input_z, out_channel_dim, False), feed_dict={input_z: example_z})
        self.plotting_images_grid(n_images, sample)
    
    def show_original_images(self, n_images):
        index = np.random.randint(self.dataset.shape[0], size=(n_images))
        sample = self.dataset.data[index]
        self.plotting_images_grid(n_images, sample)
    
    def optimization(self): # 최적화 매서드
        cases, image_width, image_height, out_channel_dim = self.dataset.shape
        input_real, input_z, labels, learn_rate = self.instantiate_inputs(image_width, image_height, out_channel_dim, self.z_dim, len(self.dataset.classes)) # 텐서플로 변수 생성
        d_loss, g_loss = self.loss(input_real, input_z, labels, out_channel_dim) # 오차
        d_vars = [v for v in tf.trainable_variables() if v.name.startswith('discriminator')] # 분류기 텐서플로 변수
        g_vars = [v for v in tf.trainable_variables() if v.name.startswith('generator')] # 생성기 텐서플로 변수
        self.g_vars = g_vars
        with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
            d_train_opt = tf.train.AdamOptimizer(self.learning_rate, self.beta1).minimize(d_loss, var_list=d_vars) # 분류기 최적화
            g_train_opt = tf.train.AdamOptimizer(self.learning_rate, self.beta1).minimize(g_loss, var_list=g_vars) # 생성기 최적화
        return input_real, input_z, labels, learn_rate, d_loss, g_loss, d_train_opt, g_train_opt
    
    def train(self, save_every_n=1000): # 학습 메서드
        losses = []
        step = 0
        epoch_count = self.epochs
        batch_size = self.batch_size
        z_dim = self.z_dim
        learning_rate = self.learning_rate
        get_batches = self.dataset.get_batches
        classes = len(self.dataset.classes)
        data_image_mode = self.dataset.image_mode
        cases, image_width, image_height, out_channel_dim = self.dataset.shape
        input_real, input_z, labels, learn_rate, d_loss, g_loss, d_train_opt, g_train_opt = self.optimization() # 최적화
        saver = tf.train.Saver(var_list=self.g_vars) # 학습 기록 객체
        rows, cols = min(5, classes), 5
        target = np.array([self.dataset.one_hot[i] for j in range(cols) for i in range(rows)])
        with tf.Session() as sess: # 세션 생성
            sess.run(tf.global_variables_initializer()) # 세션 초기화
            for epoch_i in range(epoch_count):
                for batch_images, batch_labels in get_batches(batch_size): # 배치
                    step += 1
                    batch_z = np.random.uniform(-1, 1, size=(len(batch_images), z_dim))
                    batch_z = np.concatenate((batch_z, batch_labels), axis=1)
                    batch_labels = batch_labels.reshape(batch_size, 1, 1, classes)
                    batch_labels = batch_labels * np.ones((batch_size, image_width, image_height, classes))
                    batch_images = batch_images * 2
                    _ = sess.run(d_train_opt, feed_dict={input_real: batch_images, input_z: batch_z, labels: batch_labels, learn_rate: learning_rate})
                    _ = sess.run(g_train_opt, feed_dict={input_z: batch_z, input_real: batch_images, labels: batch_labels, learn_rate: learning_rate})
                    if step % (save_every_n // 10) == 0:
                        train_loss_d = sess.run(d_loss, {input_z: batch_z, input_real: batch_images, labels: batch_labels})
                        train_loss_g = g_loss.eval({input_z: batch_z, labels: batch_labels})
                        print("Epoch %i/%i step %i..." % (epoch_i + 1, epoch_count, step),
                              "Discriminator Loss: %0.3f..." % train_loss_d,
                              "Generator Loss: %0.3f" % train_loss_g)
                    if step % save_every_n == 0:
                        rows = min(5, classes)
                        cols = 5
                        target = np.array([self.dataset.one_hot[i] for j in range(cols) for i in range(rows)])
                        self.show_generator_output(sess, rows * cols, input_z, target, out_channel_dim, data_image_mode)
                        saver.save(sess, './'+self.generator_name+'/generator.ckpt')
                try:
                    train_loss_d = sess.run(d_loss, {input_z: batch_z, input_real: batch_images, labels: batch_labels})
                    train_loss_g = g_loss.eval({input_z: batch_z, labels: batch_labels})
                    print("Epoch %i/%i step %i..." % (epoch_i + 1, epoch_count, step),
                          "Discriminator Loss: %0.3f..." % train_loss_d,
                          "Generator Loss: %0.3f" % train_loss_g)
                except:
                    train_loss_d, train_loss_g = -1, -1
                losses.append([train_loss_d, train_loss_g])
            self.show_generator_output(sess, rows * cols, input_z, target, out_channel_dim, data_image_mode)
            saver.save(sess, './' + self.generator_name + '/generator.ckpt')
        return np.array(losses)
    
    def generate_new(self, target_class=-1, rows=5, cols=5, plot=True):
        rows, cols = max(1, rows), max(1, cols)
        n_images = rows * cols
        if not self.trained: # 학습 기록이 있을 경우
            tf.reset_default_graph() # 그래프 초기화
            self._session = tf.Session() # 세션 생성
            self._classes = len(self.dataset.classes) # 클래스(분류) 수
            self._input_z = tf.placeholder(tf.float32, (None, self.z_dim + self._classes), name='input_z') # 생성된 이미지 텐서플로 변수
            out_channel_dim = self.dataset.shape[3] # 채널 수
            self._generator = self.generator(self._input_z, out_channel_dim) # 생성기
            g_vars = [v for v in tf.trainable_variables() if v.name.startswith('generator')] # 생성기 텐서플로 변수
            saver = tf.train.Saver(var_list=g_vars) # 학습 기록 객체
            print('Restoring generator graph')
            saver.restore(self._session, tf.train.latest_checkpoint(self.generator_name)) # 학습 기록 복원
            self.trained = True
        sess = self._session
        target = np.zeros((n_images, self._classes))
        for j in range(cols):
            for i in range(rows):
                if target_class == -1:
                    target[j * cols + i, j] = 1.0
                else:
                    target[j * cols + i] = self.dataset.one_hot[target_class].tolist()
        z_dim = self._input_z.get_shape().as_list()[-1]
        example_z = np.random.uniform(-1, 1, size=[n_images, z_dim - target.shape[1]])
        example_z = np.concatenate((example_z, target), axis=1)
        sample = sess.run(self._generator, feed_dict={self._input_z: example_z}) # 이미지 생성
        if plot:
            if rows * cols==1:
                if sample.shape[3] <= 1:
                    images_grid = sample[0,:,:,0]
                else:
                    images_grid = sample[0]
            else:
                images_grid = self.images_grid(sample, cols)
            plt.imshow(images_grid, cmap=self.cmap)
            plt.show()
        return sample
    
    def fit(self, learning_rate=0.0002, beta1=0.35):
        self.learning_rate = learning_rate
        self.beta1 = beta1
        with tf.Graph().as_default():
            train_loss = self.train()
        plt.plot(train_loss[:, 0], label='Discriminator')
        plt.plot(train_loss[:, 1], label='Generator')
        plt.title('Training fitting')
        plt.legend()

def main():
    '''
    labels_path = './MNIST_train-labels-idx1-ubyte.gz'
    images_path = './MNIST_train-images-idx3-ubyte.gz'
    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)
    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels), 28, 28, 1)
    batch_size = 32
    z_dim = 96
    epochs = 15
    dataset = Dataset(images, labels, channels=1)
    gan = CGan(dataset, epochs, batch_size, z_dim, generator_name='mnist')
    gan.show_original_images(25)
    gan.fit(learning_rate = 0.0002, beta1 = 0.35)
    for nclass in dataset.classes:
        print ('-'*32)
        print ('Class %i' % (nclass))
        images = gan.generate_new(nclass)
    '''
    labels_path = './train-labels-idx1-ubyte.gz'
    images_path = './train-images-idx3-ubyte.gz'
    label_names = ['t_shirt_top', 'trouser', 'pullover', 'dress', 'coat', 'sandal', 'shirt', 'sneaker', 'bag', 'ankle_boots']
    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)
    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels), 28, 28, 1)
    batch_size = 32
    z_dim = 96
    epochs = 64
    dataset = Dataset(images, labels, channels=1)
    gan = CGan(dataset, epochs, batch_size, z_dim, generator_name='zalando')
    gan.show_original_images(25)
    gan.fit(learning_rate = 0.0002, beta1 = 0.35)
    for nclass in dataset.classes:
        print ('-'*32)
        print ('Class %i' % (nclass))
        images = gan.generate_new(nclass)    
    '''
    labels_path = './gzip/emnist-balanced-train-labels-idx1-ubyte.gz'
    images_path = './gzip/emnist-balanced-train-images-idx3-ubyte.gz'
    label_names = []
    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)
    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels), 28, 28, 1)
    batch_size = 32
    z_dim = 96
    epochs = 32
    dataset = Dataset(images, labels, channels=1)
    gan = CGan(dataset, epochs, batch_size, z_dim, generator_name='emnist')
    gan.show_original_images(25)
    gan.fit(learning_rate = 0.0002, beta1 = 0.35)
    for nclass in dataset.classes:
        print ('-'*32)
        print ('Class %i' % (nclass))
        images = gan.generate_new(nclass)
    '''

if __name__ == '__main__':
    main()