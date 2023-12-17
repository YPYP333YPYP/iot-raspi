import speech_recognition as sr
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""/home/pi/git/iot-programming-with-raspi/iot-p-405100-4d785ea5814e.json"""
r = sr.Recognizer()
mic = sr.Microphone()
try:
    while True:
# microphone에서 auido source를 생성합니다
        with mic as source:
            print("Say something!")
            audio = r.listen(source)
        print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, language = 'ko',credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))