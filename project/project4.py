import RPi.GPIO as GPIO
import time
from datetime import datetime
import Adafruit_DHT
import picamera
import os

# GPIO 핀 번호 설정
PIR_PIN = 24
BULE_LED_PIN_1 = 21
BULE_LED_PIN_2 = 22
GREEN_LED_PIN = 27
BUZZER_PIN = 25
BUTTON_PIN = 12

# DHT22 센서 설정
DHT_PIN = 23

# LCD 설정 및 초기화 (Adafruit_CharLCD 라이브러리 사용)
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27) # 1번째 인자로 I2C 어댑터 모델

# 카메라 초기화
camera = picamera.PiCamera()

flag = True

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN,  GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BULE_LED_PIN_1, GPIO.OUT)
GPIO.setup(BULE_LED_PIN_2, GPIO.OUT)

GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def display_datetime_and_temperature():
    # 현재 시간 가져오기
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    # 온도 및 습도 가져오기
    time.sleep(3)
    lcd.clear()
    humidity, temperature = Adafruit_DHT.read_retry(22, DHT_PIN)
    humid = str(round(humidity,1)) # 소수점 1째자리에서 올림하고 문자화
    temp = str(round(temperature,1)) # 소수점 1째자리에서 올림하고 문자화
    print(temp,humid)
    lcd.write_string(str(current_time))
    lcd.crlf()
    lcd.write_string('T ')
    lcd.write_string(temp)
    lcd.write_string('C ')
    lcd.write_string('H ')
    lcd.write_string(humid)
    lcd.write_string('% ')
    
def capture_face():
    # 카메라로 얼굴 촬영
    camera.capture("face_capture2.jpg")

def turn_on_alarm():
    # LED 및 부저를 활성화
    GPIO.output(BULE_LED_PIN_1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BULE_LED_PIN_1, GPIO.LOW)
    GPIO.output(BULE_LED_PIN_2, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BULE_LED_PIN_2, GPIO.LOW)
    
def buzz(): # 부저를 울리는 함수
    pitch = 1000 # 주파수
    duration = 0.1 # 울리는 시간
    period = 1.0 / pitch # 소리의 진동을 만들어 내기 위한 간격
    delay = period / 2 # 간격의 절반을 delay로 설정
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(25,True)
        time.sleep(delay)
        GPIO.output(25,False)
        time.sleep(delay)    

  
# PIR 센서를 인터럽트로 설정
def pir_callback(channel):
    global flag
    flag = False
    capture_face()  
    lcd.clear()
    lcd.write_string("201935313")
    lcd.crlf()
    lcd.write_string("SeunyMyeongLee")
    
def button_callback(channel):
    global flag
    flag = True
    GPIO.output(BUZZER_PIN, False)
    GPIO.output(BULE_LED_PIN_1, False)
    GPIO.output(BULE_LED_PIN_2, False)



GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=pir_callback)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback)

try:
    while True:
        print(flag)
        time.sleep(0.1)
        if flag == True:
            display_datetime_and_temperature()
        else:
            turn_on_alarm()  
            buzz()
            

except KeyboardInterrupt:
    pass

# 정리 작업
GPIO.cleanup()