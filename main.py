import telebot
import json
from datetime import date
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

FILE = "dati.json"

cibi = {
    "uovo": 70, "uova": 70, "pane": 265,
    "pollo": 165, "tonno": 116, "yogurt": 60,
    "riso": 130, "pasta": 130, "insalata": 15,
    "mela": 52, "banana": 89
}

kcal_per_passo = 0.04

def calcola_kcal(testo):
    totale = 0
    parole = testo.lower().split(",")
    for item in parole:
        item = item.strip()
        for cibo in cibi:
            if cibo in item:
                if "g" in item:
                    try:
                        grammi = int(item.split("g")[0].strip())
                        totale += (cibi[cibo] * grammi) / 100
                    except:
                        pass
                else:
                    try:
                        numero = int(item.split()[0])
                        totale += cibi[cibo] * numero
                    except:
                        totale += cibi[cibo]
    return totale

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot attivo!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

@bot.message_handler(func=lambda message: True)
def rispondi(message):
    if message.text.lower().startswith("oggi"):
        testo = message.text.replace("oggi:", "").strip()
        kcal = calcola_kcal(testo)
        kcal_bruciare = kcal + 250
        passi = kcal_bruciare / kcal_per_passo
        tempo = passi / 100

        bot.reply_to(message, f"""
📅 Giorno salvato!
🍽 Calorie: {int(kcal)}
🔥 Da bruciare: {int(kcal_bruciare)}
🚶 Passi: {int(passi)}
⏱ Tempo: {int(tempo)} min
""")
    else:
        bot.reply_to(message, "Scrivi:\noggi: cosa hai mangiato")

bot.infinity_polling()
