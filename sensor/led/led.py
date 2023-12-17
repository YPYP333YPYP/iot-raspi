import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)


#GPIO.output(16,False)
GPIO.output(16,True)
GPIO.output(20,True)
#GPIO.output(20,False)
GPIO.output(21,True)
#GPIO.output(21,False)


input()
GPIO.cleanup()
