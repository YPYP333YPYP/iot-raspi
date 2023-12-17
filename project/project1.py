import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT) ##red
GPIO.setup(20,GPIO.OUT) ##green
GPIO.setup(21,GPIO.OUT) ##blue

GPIO.setup(17,GPIO.OUT) ##red2
GPIO.setup(27,GPIO.OUT) ##green2
GPIO.setup(22,GPIO.OUT) ##blue2

GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_UP) # BUTTON
GPIO.setup(24,GPIO.IN) # PIR
##GPIO.setup(25,GPIO.IN) # BUZZER
GPIO.setup(25,GPIO.OUT) # BUZZER

control = 0 # control 전역 변수
def buzz(): # 부저를 울리는 함수
    pitch = 1000  # 주파수
    duration = 0.1 # 울리는 시간
    period = 1.0 / pitch # 소리의 진동을 만들어 내기 위한 간격
    delay = period / 2 # 간격의 절반을 delay로 설정
    cycles = int(duration * pitch)
    pwm=GPIO.PWM(25,500)
    pwm.start(90.0)
    time.sleep(0.2)
    pwm.stop()
    pwm=GPIO.PWM(25,100)
    pwm.start(90.0)
    time.sleep(0.2)
    pwm.stop()
    
led_control=0
button_control=False
GPIO.output(16,False)
GPIO.output(17,False)
GPIO.output(20,False)
GPIO.output(21,False)
GPIO.output(22,False)
GPIO.output(27,False)
try:
    while True:
        if GPIO.input(24)==True and button_control==False:
            print("SENSOR ON!!")
            control = 1
            button_control=True
        elif GPIO.input(24)==True and button_control==Ture:
            print("senser running")
        if control == 1:
            while True:
                if (led_control==0):
                    for i in range(25):
                        buzz()
                        GPIO.output(16,True)
                        GPIO.output(17,False)
                        time.sleep(0.1)
                        GPIO.output(16,False)
                        GPIO.output(17,True)
                        time.sleep(0.1)
                        if (GPIO.input(24)==True and button_control==True):
                            print("senser already running")
                        if (GPIO.input(12)==False):
                            print("pass")
                    led_control=1
                    
                if (led_control==1):
                    GPIO.output(16,True)
                    GPIO.output(17,True)
                    GPIO.output(20,True)
                    GPIO.output(21,True)
                    GPIO.output(22,True)
                    GPIO.output(27,True)
                
                if (GPIO.input(12)==False): ##
                    GPIO.output(16,False)
                    GPIO.output(17,False)
                    GPIO.output(20,False)
                    GPIO.output(21,False)
                    GPIO.output(22,False)
                    GPIO.output(27,False)
                    control = 0
                    led_control=0
                    button_control=False
                    break
                time.sleep(0.3)
        time.sleep(0.3)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()