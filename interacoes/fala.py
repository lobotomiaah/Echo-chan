import speech_recognition as sr
import pyttsx3
import json
import os
from openai import OpenAI

# ======================
# CONFIGURAÇÃO AIMLAPI
# ======================
client = OpenAI(
    api_key="8f39166d6bcf4be89db4b126f8d21caa",  # key fictícia
    base_url="https://api.aimlapi.com/v1"
)

MODEL_NAME = "gpt-5-chat-latest"
MEMORY_FILE = "memory.json"

SYSTEM_PROMPT = """
Você é uma assistente virtual tsundere.
Você fala português brasileiro.
Você responde com personalidade, mas ajuda de verdade.
Você pode ser sarcástica, mas não ofensiva.
Você lembra informações importantes do usuário.
"""

# ======================
# MEMÓRIA
# ======================
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"name": None, "facts": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)

memory = load_memory()

def memory_context():
    text = ""
    if memory["name"]:
        text += f"O nome do usuário é {memory['name']}.\n"
    if memory["facts"]:
        text += "Informações importantes sobre o usuário:\n"
        for fact in memory["facts"]:
            text += f"- {fact}\n"
    return text

# ======================
# VOZ
# ======================
tts = pyttsx3.init()
tts.setProperty("rate", 180)

def speak(text):
    tts.say(text)
    tts.runAndWait()

# ======================
# OUVIR MICROFONE
# ======================
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Fale algo...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="pt-BR")
        print("🗣 Você:", text)
        return text
    except:
        return ""

# ======================
# GPT
# ======================
def ask_gpt(user_text):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n" + memory_context()},
        {"role": "user", "content": user_text}
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.8
    )

    return response.choices[0].message.content

# ======================
# MEMORIZAR COISAS
# ======================
def check_memory(user_text):
    text = user_text.lower()

    if "meu nome é" in text:
        name = user_text.split("meu nome é")[-1].strip()
        memory["name"] = name
        save_memory(memory)
        speak(f"Hmpf… então seu nome é {name}. Vou lembrar disso.")

    if "lembra que" in text:
        fact = user_text.split("lembra que")[-1].strip()
        memory["facts"].append(fact)
        save_memory(memory)
        speak("Tsc… tá bom, vou guardar isso.")

# ======================
# LOOP PRINCIPAL
# ======================
speak("Tsc… ligou o sistema. Não pense que eu estava esperando.")

while True:
    user_text = listen()

    if not user_text:
        speak("Hã? Fala direito, baka.")
        continue

    if "sair" in user_text.lower():
        speak("T-tanto faz… até mais.")
        break

    check_memory(user_text)

    reply = ask_gpt(user_text)
    print("🤖 IA:", reply)
    speak(reply)