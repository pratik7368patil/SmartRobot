import speech_recognition as sr
import pyttsx3


engine = pyttsx3.init()
r = sr.Recognizer()


def Recognize_voice():
    with sr.Microphone() as source:
        while 1:
            engine.runAndWait()
            print('now say  >>>>>')
            audio = r.listen(source)
            try:
                _data = r.recognize_google(audio)
                print('You said : {}'.format(_data))
                return _data
                break
            except:
                print('Sorry could not recognize your voice')
                engine.say('Sorry could not recognize your voice, Please say it again')
                engine.runAndWait()
