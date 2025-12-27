import sounddevice as sd
import numpy as np
import torch
import torchaudio
from faster_whisper import WhisperModel
import queue
import threading
import time
from config import WHISPER_MODEL

# Carrega Silero VAD
model_vad, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                  model='silero_vad',
                                  force_reload=False,
                                  onnx=False)  # Use ONNX se quiser mais rápido

(get_speech_timestamps, _, read_audio, _, _) = utils

# Configs
samplerate = 16000
blocksize = 512  # Pequeno pra baixa latência
audio_queue = queue.Queue()
recording = False
audio_buffer = []

whisper_model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")  # Leve pra CPU

def callback(indata, frames, time, status):
    global recording, audio_buffer
    audio_queue.put(indata.copy())

def vad_thread():
    global recording, audio_buffer
    buffer_seconds = 30  # Buffer máximo de 30s
    while True:
        if not audio_queue.empty():
            data = audio_queue.get()
            audio_float = data.flatten().astype(np.float32)
            # Detecta voz no chunk atual
            if model_vad(torch.from_numpy(audio_float), samplerate).item() > 0.5:
                if not recording:
                    print("🎤 Detectei voz! Gravando...")
                    recording = True
                audio_buffer.append(audio_float)
            else:
                if recording:
                    # Silêncio após fala → processa
                    full_audio = np.concatenate(audio_buffer)
                    if len(full_audio) > samplerate * 0.5:  # Pelo menos 0.5s de fala
                        print("⏹️ Fim da fala. Processando...")
                        transcribe_audio(full_audio)
                    recording = False
                    audio_buffer = []
            # Limita buffer
            if len(audio_buffer) * blocksize / samplerate > buffer_seconds:
                audio_buffer = audio_buffer[-int(buffer_seconds * samplerate / blocksize):]

def transcribe_audio(audio_np):
    # Salva temporário pra Whisper
    import wave
    with wave.open("audio/temp.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes((audio_np * 32767).astype(np.int16).tobytes())
    
    segments, _ = whisper_model.transcribe("audio/temp.wav", language="pt")
    texto = " ".join(seg.text for seg in segments).strip()
    print("Você:", texto)
    return texto

def start_listening():
    print("Echo-sama sempre escutando! Fale quando quiser~ (Ctrl+C pra parar)")
    threading.Thread(target=vad_thread, daemon=True).start()
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='float32',
                        blocksize=blocksize, callback=callback):
        while True:
            time.sleep(0.1)  # Mantém vivo

# Função que main.py chama (agora retorna texto quando detecta fala)
def listen_continuously():
    return start_listening()  # Não retorna texto, mas processa internamente