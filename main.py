import json, pyaudio, requests
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import eel
import pygame


model = Model('model')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def gpt(prompt):
    options = {
    'method': 'POST',
    'url': 'https://open-ai21.p.rapidapi.com/chatgpt',
    'headers': {
        'content-type': 'application/json',
        'X-RapidAPI-Key': '43631ce4f1msh20404de13215b39p1dc626jsn3ef12746d123',
        'X-RapidAPI-Host': 'open-ai21.p.rapidapi.com'
    },
    'json': {
        'messages': [
            {
                'role': 'user',
                'content': prompt 
            }
        ],
        'web_access': False
        }
    }

    response = requests.request(**options)
    return response.json()


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
    for text in listen():
        return text
    
@eel.expose
def send(text):
    print(text)
    gpt_text = gpt(text)['result']
    print(gpt_text)
    tts = gTTS(gpt_text, lang='ru')
    tts.save('voice.mp3')
    pygame.init()
    song = pygame.mixer.Sound('voice.mp3')
    clock = pygame.time.Clock()
    song.play()
    return gpt_text




eel.init('web')
eel.start('index.html', size=(430, 500))

    
