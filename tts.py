import requests
import pygame
import time
import os

# Config API (porta padrão do GPT-SoVITS API)
API_URL = "http://127.0.0.1:9872/inference"  # Mude se sua porta for diferente

# Path do seu arquivo de voz clonada de Meisho Doto (o .wav de referência)
REFERENCE_AUDIO = "voice/meisho_doto_reference.wav"  # Coloque seu .wav aqui

def falar(texto):
    print("Echo-sama falando:", texto)
    
    payload = {
        "text": texto,
        "text_lang": "zh",  # Chinês pra emoção anime, funciona com PT
        "ref_audio_path": REFERENCE_AUDIO,
        "prompt_lang": "ja",  # Japonês pra tom tsundere
        "top_k": 5,
        "top_p": 1.0,
        "temperature": 1.0,
        "speed": 1.0
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            with open("output/output.wav", "wb") as f:
                f.write(response.content)
            
            pygame.mixer.init()
            pygame.mixer.music.load("output/output.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        else:
            print("Erro na API:", response.text)
    except Exception as e:
        print("Erro ao conectar API:", e)