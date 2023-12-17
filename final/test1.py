# 보이스 인식을 사용하여 단어에 따라 LED 작동 방식 변경, 인터럽트 방식으로 버튼 클릭 시 카메라로 노트븍 모니터 사진 찍기
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

from picamera import PiCamera

import speech_recognition as sr
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""/home/pi/git/iot-programming-with-raspi/iot-p-405100-4d785ea5814e.json"""

red_led_pin = 16 # 36
blue_led_pin = 20 # 38
green_led_pin = 21 # 40
button_pin = 12 # 32

GPIO.setup(red_led_pin,GPIO.OUT)
GPIO.setup(blue_led_pin,GPIO.OUT)
GPIO.setup(green_led_pin,GPIO.OUT)

camera = PiCamera()
camera.resolution = (2592, 1944)




def button_callback(chaneel):
    camera.capture('example.jpg') 

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback)



r = sr.Recognizer()
mic = sr.Microphone()
try:
    while True:
        with mic as source:
            print("Say something!")
            audio = r.listen(source)
        gcSTT = r.recognize_google_cloud(audio, language = 'ko',credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        if gcSTT == "불 켜":
            GPIO.output(red_led_pin, True)
        if gcSTT == "불 꺼":
            GPIO.output(red_led_pin, False)
            
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))
except KeyboardInterrupt:
    GPIO.cleanup()    
    camera.close()