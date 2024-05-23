import json, pyaudio, requests
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import os
import eel
import pygame


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
    

@eel.expose
def start_listen():
    print('Start listening...')
    listen()
    gpt_text = None
    for text in listen():
        print(text)
        gpt_text = gpt(f'{text}')
        print(gpt_text)
        tts = gTTS(gpt_text, lang='ru')
        tts.save('voice.mp3')
        pygame.init()
        song = pygame.mixer.Sound('voice.mp3')
        clock = pygame.time.Clock()
        song.play()
        return gpt_text
    
@eel.expose
def send(text):
    print(text)
    gpt_text = gpt(text)
    print(gpt_text)
    tts = gTTS(gpt_text, lang='ru')
    tts.save('voice.mp3')
    pygame.init()
    song = pygame.mixer.Sound('voice.mp3')
    clock = pygame.time.Clock()
    song.play()
    return gpt_text




eel.init('web')
eel.start('index.html', size=(500, 500))
    