import customtkinter as ctk
import speech_recognition as sr
import requests
from gtts import gTTS
from playsound import playsound
import threading
import time
import os

# ------------ Appearance ------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🌤️ Wavy - Weather Bot")
app.geometry("500x500")
app.resizable(False, False)

user_lang = "hi"
tts_lang = "hi"

API_KEY = "paste your own API"

# ------------ Speak Function ------------
def speak(text):
    try:
        tts = gTTS(text=text, lang=tts_lang)
        filename = "voice.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print("TTS error:", e)

# ------------ Animated Text ------------
def animated_text(text):
    output_label.configure(text="")
    def run():
        for i in range(len(text) + 1):
            output_label.configure(text=text[:i])
            time.sleep(0.03)
    threading.Thread(target=run, daemon=True).start()

# ------------ Weather Fetch ------------
def get_weather(city):
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": API_KEY, "units": "metric", "lang": user_lang}
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            result = f"{city} mein abhi {temp}°C hai aur mausam: {desc}" if user_lang == "hi" else f"It is {temp}°C in {city} with {desc}."
            animated_text(result)
            threading.Thread(target=speak, args=(result,), daemon=True).start()
        else:
            error = "Sheher galat hai ya API mein dikkat hai." if user_lang == "hi" else "City name is incorrect or API issue."
            animated_text(error)
            threading.Thread(target=speak, args=(error,), daemon=True).start()
    except:
        animated_text("Network error.")
        threading.Thread(target=speak, args=("Network error.",), daemon=True).start()

# ------------ Button Handlers ------------
def type_input():
    city = city_entry.get()
    if city:
        get_weather(city)

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        animated_text("🎙 Listening...")
        threading.Thread(target=speak, args=("Sheher ka naam boliye." if user_lang == "hi" else "Please say the city name",), daemon=True).start()
        try:
            audio = recognizer.listen(source, timeout=5)
            city = recognizer.recognize_google(audio, language="hi-IN" if user_lang == "hi" else "en-IN")
            city_entry.delete(0, ctk.END)
            city_entry.insert(0, city)
            get_weather(city)
        except:
            msg = "Samajh nahi aaya. Phir se boliye." if user_lang == "hi" else "Sorry, I didn’t catch that."
            animated_text(msg)
            threading.Thread(target=speak, args=(msg,), daemon=True).start()

# ------------ Language Selection ------------
def select_language(lang):
    global user_lang, tts_lang
    user_lang = lang
    tts_lang = 'hi' if lang == 'hi' else 'en'
    lang_window.destroy()

    if lang == "hi":
        intro1 = "Namaste! Main Wavy Weather Bot hoon."
        intro2 = "Upar button se sheher likhiye ya mic dabaiye."
    else:
        intro1 = "Hello! I'm Wavy – your weather bot."
        intro2 = "Type your city or click mic to speak."

    def speak_intro():
        animated_text(intro1)
        speak(intro1)
        time.sleep(1.5)
        animated_text(intro2)
        speak(intro2)

    threading.Thread(target=speak_intro, daemon=True).start()

# ------------ Prompt Language Selection ------------
def show_language_prompt():
    global lang_window
    lang_window = ctk.CTkToplevel(app)
    lang_window.title("Select Language")
    lang_window.geometry("300x150")
    lang_window.grab_set()

    threading.Thread(target=speak, args=("Output kis language mein chahiye? Hindi ya English?",), daemon=True).start()

    label = ctk.CTkLabel(lang_window, text="Select Output Language", font=("Arial", 16))
    label.pack(pady=10)

    btn_hi = ctk.CTkButton(lang_window, text="Hindi", command=lambda: select_language("hi"))
    btn_hi.pack(pady=5)

    btn_en = ctk.CTkButton(lang_window, text="English", command=lambda: select_language("en"))
    btn_en.pack(pady=5)

# ------------ GUI Layout ------------
title_label = ctk.CTkLabel(app, text="🌤️ Wavy Weather Bot", font=("Helvetica", 24, "bold"))
title_label.pack(pady=20)

city_entry = ctk.CTkEntry(app, width=300, placeholder_text="Type city name here...")
city_entry.pack(pady=10)

btn_get = ctk.CTkButton(app, text="📩 Get Weather", command=type_input)
btn_get.pack(pady=10)

btn_mic = ctk.CTkButton(app, text="🎤 Speak City Name", command=voice_input)
btn_mic.pack(pady=10)

output_label = ctk.CTkLabel(app, text="", wraplength=400, font=("Helvetica", 16))
output_label.pack(pady=30)

# ------------ Start ------------
show_language_prompt()
app.mainloop()
