import RPi.GPIO as GPIO
import time
# PIR 감지 콜백함수
def pirDetected(channel):
    print('channel %s PIR detected!!'%channel)
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # UP이면 PIR 감지 안될때 on, 감지될때 off
# interrupt 선언
GPIO.add_event_detect(24, GPIO.FALLING, callback=pirDetected) # RISING, FALLING, BOTH 
# 메인 쓰레드
try:
    while 1:
        print(".")
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
