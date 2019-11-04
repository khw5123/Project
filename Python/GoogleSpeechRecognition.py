# -*- coding: utf-8 -*-
import speech_recognition as sr

# http://blog.naver.com/PostView.nhn?blogId=post_human&logNo=220496837737&parentCategoryNo=&categoryNo=31&viewDate=&isShowPopularPosts=true&from=search

def googleSpeechRecognition():
    while True:
        try:
            r = sr.Recognizer() # obtain audio from the microphone
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)
            # recognize speech using Google Speech Recognition
            try:
                print("[+] " + r.recognize_google(audio) + "\n")
            except sr.UnknownValueError:
                print("[-] Google Speech Recognition could not understand audio\n")
        except Exception as e:
            print('[-] ' + str(e))

def main():
    googleSpeechRecognition()

if __name__ == '__main__':
    main()