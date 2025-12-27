import threading
import queue
import time
import numpy as np
import sounddevice as sd
import torch
from faster_whisper import WhisperModel
import wave
import os

from llm import load_memory, gerar_resposta
from tts import falar
from config import WHISPER_MODEL

# Configs
SAMPLERATE = 16000
BLOCKSIZE = 512

# Carrega Silero VAD (leve e rápido)
model_vad, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                  model='silero_vad',
                                  force_reload=False,
                                  trust_repo=True)

(get_speech_timestamps, _, read_audio, _, _) = utils

# Whisper
whisper_model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")

# Memória
history = load_memory()

# Buffer
audio_queue = queue.Queue()
speech_buffer = []
recording = False
last_speech_time = time.time()

# Ajustes pra menos ruído falso e resposta rápida
SPEECH_THRESHOLD = 0.75
MIN_SPEECH_DURATION = 0.5
MIN_SILENCE_DURATION = 0.8

print("Echo-sama tsundere pronta! 💢❤️")
print("Eu estou escutando o tempo todo agora~ Fale claro quando quiser (eu detecto automaticamente)!")
print("Diga algo como 'Oi Echo-sama' pra testar... (Ctrl+C pra parar)")

def audio_callback(indata, frames, time_info, status):
    audio_queue.put(indata.copy())

def vad_processor():
    global recording, speech_buffer, last_speech_time
    
    while True:
        if not audio_queue.empty():
            data = audio_queue.get()
            audio_float32 = data.flatten()
            
            speech_prob = model_vad(torch.from_numpy(audio_float32), SAMPLERATE).item()
            
            if speech_prob > SPEECH_THRESHOLD:
                if not recording:
                    print("🎤 Ouvi você! Gravando...")
                    recording = True
                speech_buffer.append(audio_float32)
                last_speech_time = time.time()
            else:
                if recording and (time.time() - last_speech_time > MIN_SILENCE_DURATION):
                    process_speech()
                    recording = False
                    speech_buffer = []
        
        time.sleep(0.01)

def process_speech():
    global history
    
    if not speech_buffer:
        return
    
    full_audio = np.concatenate(speech_buffer)
    duration = len(full_audio) / SAMPLERATE
    
    if duration < MIN_SPEECH_DURATION:
        return  # Ignora barulhinho curto
    
    # Cria pasta audio se não existir
    if not os.path.exists("audio"):
        os.makedirs("audio")
    
    with wave.open("audio/temp.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLERATE)
        wf.writeframes((full_audio * 32767).astype(np.int16).tobytes())
    
    segments, _ = whisper_model.transcribe("audio/temp.wav", language="pt")
    user_msg = " ".join(seg.text for seg in segments).strip()
    
    if not user_msg:
        return
    
    print("Você:", user_msg)
    
    resposta = gerar_resposta(user_msg, history)
    print("Echo-sama:", resposta)
    falar(resposta)

# Inicia tudo
threading.Thread(target=vad_processor, daemon=True).start()

with sd.InputStream(samplerate=SAMPLERATE, channels=1, dtype='float32',
                    blocksize=BLOCKSIZE, callback=audio_callback):
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nTchau, baka senpai... volta logo, idiota! 💢")