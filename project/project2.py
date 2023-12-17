import tkinter as tk
from tkinter import Scale
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
from matplotlib.figure import Figure


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

tones = {
    "B0": 31,
    "C1": 33,
    "CS1": 35,
    "D1": 37,
    "DS1": 39,
    "E1": 41,
    "F1": 44,
    "FS1": 46,
    "G1": 49,
    "GS1": 52,
    "A1": 55,
    "AS1": 58,
    "B1": 62,
    "C2": 65,
    "CS2": 69,
    "D2": 73,
    "DS2": 78,
    "E2": 82,
    "F2": 87,
    "FS2": 93,
    "G2": 98,
    "GS2": 104,
    "A2": 110,
    "AS2": 117,
    "B2": 123,
    "C3": 131,
    "CS3": 139,
    "D3": 147,
    "DS3": 156,
    "E3": 165,
    "F3": 175,
    "FS3": 185,
    "G3": 196,
    "GS3": 208,
    "A3": 220,
    "AS3": 233,
    "B3": 247,
    "C4": 262,
    "CS4": 277,
    "D4": 294,
    "DS4": 311,
    "E4": 330,
    "F4": 349,
    "FS4": 370,
    "G4": 392,
    "GS4": 415,
    "A4": 440,
    "AS4": 466,
    "B4": 494,
    "C5": 523,
    "CS5": 554,
    "D5": 587,
    "DS5": 622,
    "E5": 659,
    "F5": 698,
    "FS5": 740,
    "G5": 784,
    "GS5": 831,
    "A5": 880,
    "AS5": 932,
    "B5": 988,
    "C6": 1047,
    "CS6": 1109,
    "D6": 1175,
    "DS6": 1245,
    "E6": 1319,
    "F6": 1397,
    "FS6": 1480,
    "G6": 1568,
    "GS6": 1661,
    "A6": 1760,
    "AS6": 1865,
    "B6": 1976,
    "C7": 2093,
    "CS7": 2217,
    "D7": 2349,
    "DS7": 2489,
    "E7": 2637,
    "F7": 2794,
    "FS7": 2960,
    "G7": 3136,
    "GS7": 3322,
    "A7": 3520,
    "AS7": 3729,
    "B7": 3951,
    "C8": 4186,
    "CS8": 4435,
    "D8": 4699,
    "DS8": 4978
}
melody = ["C4", "D4", "E4", "C4", "E4", "F4", "G4", "A4", "C4", "D4", "E4", "C4"]


R_PIN = 16
G_PIN = 20
B_PIN = 21
P_PIN = 24
R_PIN_2 = 17
G_PIN_2 = 27
B_PIN_2 = 22

DHT_PIN = 23

BUTTON_PIN = 12
BUZZER_PIN = 25


blink_toggle = False
r_toggle = True
g_toggle = True
b_toggle = True

pir_count = 0
btn_count = 0

GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)
GPIO.setup(R_PIN_2, GPIO.OUT)
GPIO.setup(G_PIN_2, GPIO.OUT)
GPIO.setup(B_PIN_2, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm_red = GPIO.PWM(R_PIN, 100)
pwm_blue = GPIO.PWM(B_PIN, 100)
pwm_green = GPIO.PWM(G_PIN, 100)

#GPIO.setup(pwm_red, GPIO.OUT)
#GPIO.setup(pwm_green, GPIO.OUT)
#GPIO.setup(pwm_blue, GPIO.OUT)



root = tk.Tk()
root.title("Sensor Control")

# 창 크기 설정
root.geometry("1280x800")


def on_button_click_red():
    global r_toggle
    if r_toggle == True:
        GPIO.output(16, True)
        r_toggle = False
    elif r_toggle == False:
        GPIO.output(16, False)
        r_toggle = True


def on_button_click_blue():
    global b_toggle
    if b_toggle == True:
        GPIO.output(21, True)
        b_toggle = False
    elif b_toggle == False:
        GPIO.output(21, False)
        b_toggle = True


def on_button_click_green():
    global g_toggle
    if g_toggle == True:
        GPIO.output(20, True)
        g_toggle = False
    elif g_toggle == False:
        GPIO.output(20, False)
        g_toggle = True


def slider_changed(value):
    duty_cycle = int(value)
    if r_toggle == True:
        pwm_red.start(0)
        pwm_red.ChangeDutyCycle(duty_cycle)
    
    if g_toggle == True:
        pwm_green.start(0)
        pwm_green.ChangeDutyCycle(duty_cycle)
    
    if b_toggle == True:
        pwm_blue.start(0)
        pwm_blue.ChangeDutyCycle(duty_cycle)
 


def on_button_blink():
    global blink_toggle

    if blink_toggle:
        GPIO.output(R_PIN, GPIO.LOW)
        GPIO.output(G_PIN, GPIO.LOW)
        GPIO.output(B_PIN, GPIO.LOW)
        blink_toggle = False
        return

    r_state = GPIO.input(R_PIN)
    g_state = GPIO.input(G_PIN)
    b_state = GPIO.input(B_PIN)

    if r_state == GPIO.HIGH:
        GPIO.output(R_PIN, GPIO.LOW)
    if g_state == GPIO.HIGH:
        GPIO.output(G_PIN, GPIO.LOW)
    if b_state == GPIO.HIGH:
        GPIO.output(B_PIN, GPIO.LOW)

    time.sleep(2)

    if r_state == GPIO.HIGH:
        GPIO.output(R_PIN, GPIO.HIGH)
    if g_state == GPIO.HIGH:
        GPIO.output(G_PIN, GPIO.HIGH)
    if b_state == GPIO.HIGH:
        GPIO.output(B_PIN, GPIO.HIGH)

    blink_toggle = True


def pir_callback(channel):
    global pir_count
    print(pir_count)
    if GPIO.input(P_PIN) == GPIO.HIGH:
        pir_label.config(text="PIR: Motion Detected")
        GPIO.output(R_PIN, GPIO.HIGH)

        if pir_count >= 2:

            for _ in range(5):
                GPIO.output(R_PIN, GPIO.LOW)
                time.sleep(0.5)
                GPIO.output(R_PIN, GPIO.HIGH)
                time.sleep(0.5)

            pir2_label.config(text="PIR2: Motion Detected")
            pir_count = 0
        else:
            pir_count += 1
    else:

        pir_label.config(text="PIR: No Motion")
        GPIO.output(R_PIN, GPIO.LOW)


def button_callback(channel):
    global btn_count
    if btn_count == 0:
        # First button press: Activate the buzzer
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        switch_label.config(text="Switch: push !!")
        btn_count +=1

    elif btn_count == 1:
        GPIO.output(R_PIN, GPIO.LOW)
        GPIO.output(G_PIN, GPIO.LOW)
        GPIO.output(B_PIN, GPIO.LOW)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

        
        switch2_label.config(text="Switch2: push !!")
        btn_count = 0

def play_note(note):
    if note in tones:
        frequency = tones[note]
        p = GPIO.PWM(BUZZER_PIN, frequency)
        p.start(50)  
        time.sleep(0.5) 
        p.stop()  
        time.sleep(0.1)  

def play_music():
    for note in melody:
        play_note(note)


def stop_sensors():
    GPIO.cleanup()        


temperature_data = [1,2,3,4,5]
humidity_data = [10,20,30,40]

def collect_data():
    humidity, temperature = Adafruit_DHT.read_retry(22, DHT_PIN)
    #if humidity is not None and temperature is not None:
        #temperature_data.append(int(temperature))
        #humidity_data.append(int(humidity))
       
    root.after(1000, collect_data)


from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)
def custome_method2():
    # 입력된 비밀번호 가져오기
    entered_password = password_entry.get()
    
    # 비밀번호 확인 및 LED 제어
    if entered_password == "201935313":
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(16, GPIO.LOW)
        lcd.clear()
        lcd.write_string('OPEN')
    else:
        GPIO.output(20, GPIO.LOW)
        GPIO.output(16, GPIO.HIGH)
        lcd.clear()
        lcd.write_string('WRONG PASSWORD')
GPIO.setup(P_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # UP이면 PIR 감지 안될때 on, 감지될때 off
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(P_PIN, GPIO.RISING, callback=pir_callback)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING,
                      callback=button_callback, bouncetime=300)


button_frame = tk.Frame(root)
button_frame.grid(row=0, column=0)

slider_frame = tk.Frame(root)
slider_frame.grid(row=1, column=0)

label_frame = tk.Frame(root)
label_frame.grid(row=2, column=0)

# 버튼 생성
r_button = tk.Button(button_frame, text="R",
                     command=on_button_click_red)
g_button = tk.Button(button_frame, text="G",
                     command=on_button_click_green)
b_button = tk.Button(button_frame, text="B",
                     command=on_button_click_blue)
i_button = tk.Button(button_frame, text="I",
                    command=on_button_blink)
s_button = tk.Button(button_frame, text="S",
                     command=play_music)
x_button = tk.Button(button_frame, text="X",
                     command=stop_sensors)


# 라벨 생성
pir_label = tk.Label(label_frame, text="PIR: ")
pir2_label = tk.Label(label_frame, text="PIR2: ")
switch_label = tk.Label(label_frame, text="Switch: ")
switch2_label = tk.Label(label_frame, text="Switch2: ")

# 슬라이더 생성
m_slider = Scale(slider_frame, from_=0, to=100,
                 orient="horizontal", label="M", command=slider_changed)

# 버튼 및 라벨 배치
r_button.grid(row=0, column=0)
g_button.grid(row=0, column=1)
b_button.grid(row=0, column=2)
i_button.grid(row=0, column=3)
s_button.grid(row=0, column=4)
x_button.grid(row=0, column=5)



pir_label.grid(row=0, column=0)
pir2_label.grid(row=1, column=0)
switch_label.grid(row=2, column=0)
switch2_label.grid(row=3, column=0)

# 슬라이더 배치
m_slider.grid(row=0, column=0)

label = tk.Label(root, text="Enter Password:")
label.grid(row=8, column=0)

password_entry = tk.Entry(root, show="*")  # 비밀번호는 '*'로 표시
password_entry.grid(row=8, column=1)

c2_button = tk.Button(button_frame, text="Custom2",
                     command=custome_method2)

c2_button.grid(row=8, column=2)

# 메인 루프 실행
root.mainloop()
