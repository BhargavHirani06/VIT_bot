import pvporcupine
import pyaudio
import struct
import subprocess
import pyttsx3

handle = pvporcupine.create(
    access_key='jAhJIPDbdOkbpJKt9zF4/pF/v5o179vd7kSOQnoj4BNfC/g==',
    keyword_paths=['Hey-navigate-me_en_windows_v2_1_0.ppn']
    
    )


pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=handle.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=handle.frame_length)

engine = pyttsx3.init()

while True:
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)

    keyword_index = handle.process(pcm)
    if keyword_index >= 0:
        print("Detected")
        print("Hello, my name is Navit. How may I assist you")
        engine.say("Hello, my name is Navit. How may I assist you?")
        engine.runAndWait()
        subprocess.Popen(["python", "chatbot.py"])

        while True:
            pcm = audio_stream.read(handle.frame_length)
            pcm = struct.unpack_from("h" * handle.frame_length, pcm)

            keyword_index = handle.process(pcm)
            if keyword_index >= 0:
                print("Detected")
                break


     
