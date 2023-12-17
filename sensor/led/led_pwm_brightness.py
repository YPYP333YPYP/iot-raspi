import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
pwm_led = GPIO.PWM(16, 500)  # GPIO.PWM(pin_num,frequency(hz)
pwm_led.start(0)
try:
    while True:
        for i in range(0, 101, 5):  # 출력을 0부터 100까지
            pwm_led.ChangeDutyCycle(i)  # 출력 변경
            time.sleep(0.2)
        for i in range(100, -1, -5):  # 출력을 100부터 0까지
            pwm_led.ChangeDutyCycle(i)  # 출력 변경
            time.sleep(0.2)
except KeyboardInterrupt:
    pass
finally:
    pwm_led.stop()
    GPIO.cleanup()  
