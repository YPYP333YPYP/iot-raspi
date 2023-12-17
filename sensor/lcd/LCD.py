from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27) # 1번째 인자로 I2C 어댑터 모델
# 2번째 인자로 LCD의 주소를 전달
lcd.write_string('Hello') # Hello 글자 출력
lcd.crlf() # 한줄 띄기
lcd.write_string('world!') 