# Home Control System의 동작 방식에 대한 설명
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT) # LED R
dht_type = 22 # DHT 타입
bcm_pin = 23 # 핀 번호
lcd = CharLCD('PCF8574',0x27)
normal_temperature = 27
try:
    while True:
        time.sleep(3)
        lcd.clear()
        humidity, temperature = Adafruit_DHT.read_retry(dht_type, bcm_pin)
        humid = round(humidity,1) # 소수점 1째자리에서 올림하고 문자화
        temp = round(temperature,1) # 소수점 1째자리에서 올림하고 문자화
        print(temp,humid)
        if temp>normal_temperature:
            lcd.write_string("201935313") # 학번
            lcd.crlf()
            lcd.write_string("Need Cooling")
            GPIO.output(16,True)
        else:
            GPIO.output(16,False)
            lcd.write_string('TEMP ')
            lcd.write_string(str(temp))
            lcd.write_string('C ')
            lcd.crlf()
            lcd.write_string('HUMID ')
            lcd.write_string(str(humid))
            lcd.write_string('% ')
except KeyboardInterrupt:
    GPIO.cleanup() # 프로그램 종료 시 LCD 화면의 문자를 지움
    lcd.clear()
