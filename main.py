import json, pyaudio, requests
from vosk import Model, KaldiRecognizer
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
en_voice_id = 'HKEY_LOCAL_MACHINE'
for voice in voices:
    print(voice)
model = Model('model')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']
print('Start listening...')
for text in listen():
    print(text)
    r = requests.post("https://chat-gpt.org/api/text", data={"message": f"{text}","recaptcha_token":"0.SE6n8Q6TA6XjfTeau5SZWv5LsG7frHdshSym2nND07fPSY0Db3uEk9Pnfv6ex_MtjiEF5IclAqxiq1DTaKov-fe3BJCNN-V-Zmow15JUHaY1y0f9nwuBz35Zmq_I0OdYH9Z_n8SUM0-ZhDC6SkURS5_1dg-2ytCTtnBxbG1CdmKknkXrx4YDOjHmBgffoENgmgsDuL3jTUZBbyrksA1DmkgOXKu7qFj-05T3Ie4IWo4XBkECa7kYB4pIO64PqK79ZiMtfdvclBJIJwkgMvAdGomvSor-SCR2SbzdBHHhO5CFeNgVvhXKih7DNgFiO8XRpNUoFhgryRSlYSP2grk9xaqR4v6H51jqJCM4UNCO1Ve04YMb7votAkMapybdGmAW0zb6blL0L1qwe4HANgGRpWG2j7Mu7Efnn2Wb7OVlfWoAVa5XnZnMdJFe-XSqoFXW.EBYHE7tLYhkH4erPfqbEjw.004171266ddaadab20f0c3153a7fb1b339ec37983f0df3e19d45d511e8e79a42","temperature":1,"presence_penalty":0,"top_p":1,"frequency_penalty":0})
    print(r.json())