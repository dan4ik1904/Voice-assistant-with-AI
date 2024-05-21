import json, pyaudio, requests
from vosk import Model, KaldiRecognizer
import pyttsx3
from gtts import gTTS
import os


gpt_token= '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'

model = Model('model')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def gpt(prompt):
    r = requests.get(f'http://localhost:3000?text={prompt}')
    print(r.json())
    return r.json()['result']


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
    gpt_text = gpt(f'{text}')
    print(gpt_text)
    tts = gTTS(gpt_text, lang='ru')
    tts.save('voice.mp3')
    os.system("voice.mp3")
    


listen()
    