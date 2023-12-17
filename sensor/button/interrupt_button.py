import RPi.GPIO as GPIO
import time
# 스위치 눌렸을 때 콜백함수
def switchPressed(channel):
    print('channel %s pressed!!'%channel)
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # DOWN이면 BUTTON 입력 스위치 안눌렸을 때 off, 눌렸을 때 on
# interrupt 선언
GPIO.add_event_detect(12, GPIO.RISING, callback=switchPressed) # RISING, FALLING, BOTH 
# 메인 쓰레드
try:
    while True:
        print(".")
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()