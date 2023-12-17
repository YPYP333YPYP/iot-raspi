import RPi.GPIO as GPIO
import time
buzzer = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)
#GPIO.setwarnings(False)
pwm=GPIO.PWM(buzzer, 700) # ‘261’는 음의 높이에 해당하는 특정 주파수
pwm.start(50.0) # '90' dutyCycle (0 ~ 100 %)
time.sleep(3.0) # 3초간 음이 울리도록 지연
pwm.stop()
GPIO.cleanup()
