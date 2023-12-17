import RPi.GPIO as GPIO
import time
global control
control = False
# 스위치 눌렸을 때 콜백함수
def switchPressed(channel):
    global control
    print('channel %s pressed!!'%channel)
    if(control==True): # Toggle
        control=False
        GPIO.output(16,True)
    else:
        control=True
        GPIO.output(16,False)
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # DOWN이면 BUTTON 입력 스위치 안눌렸을 때 off, 눌렸을 때 on
GPIO.add_event_detect(12, GPIO.RISING, callback=switchPressed) # RISING, FALLING, BOTH 
# 메인 쓰레드
try:
    while 1:
        print(".")
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
