# tts.py - Versão 100% estável (configura channels e sample_rate manualmente)

import wave
import pygame
import os
from piper.voice import PiperVoice

MODEL_PATH = "voice/en_US-amy-medium.onnx"  # Voz fofa Amy!

voice = PiperVoice.load(MODEL_PATH)

def falar(texto):
    print("Echo-sama falando:", texto)
    
    # Cria pasta output se não existir
    if not os.path.exists("output"):
        os.makedirs("output")
    
    output_path = "output/output.wav"
    
    with wave.open(output_path, "wb") as wav_file:
        # Configura manualmente (Piper usa sempre mono 16-bit)
        wav_file.setnchannels(1)                # 1 canal (mono)
        wav_file.setsampwidth(2)                # 16-bit (2 bytes)
        wav_file.setframerate(voice.config.sample_rate)  # Sample rate do modelo (ex: 22050 pra Amy medium)
        
        # Agora Piper escreve os dados de áudio
        voice.synthesize(texto, wav_file)
    
    # Toca o WAV gerado
    pygame.mixer.init()
    pygame.mixer.music.load(output_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)