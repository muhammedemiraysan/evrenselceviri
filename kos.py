#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pyaudio
from translate import Translator
import os
from gtts import gTTS, lang
import wave
import wavio
import os
import soundfile as sf
from pocketsphinx import AudioFile, get_model_path, get_data_path
import speech_recognition as sr
r = sr.Recognizer()
Buton = 4
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Buton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
translator = Translator(to_lang='tr')
result = "1"
while True:
    buton_durum = GPIO.input(Buton) 
    filename = "output.wav"
    file = sr.AudioFile('output.wav')
    while buton_durum == 1:
        buton_durum = GPIO.input(Buton)
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second
        seconds = 3
        filename = "output.wav"

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

# Stop and close the stream 
        stream.stop_stream()
        stream.close()
# Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')

# Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        with file as source:
            try:    
                r.adjust_for_ambient_noise(source)
                audio = r.record(source)
                result = r.recognize_google(audio,language='en')
                print(result)
            except sr.UnknownValueError:
                print("ne dedigini anlayamadim")
        translation = translator.translate(result)
        if (result != "1"):
            print(translation)
            ses = gTTS(text=translation,lang='tr',slow=False)
            ses.save("ses.mp3")
            os.system(f"cvlc --play-and-exit ses.mp3")
        result = "1"   
                                   
