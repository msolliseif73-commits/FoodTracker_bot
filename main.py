# main.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from database import init_db, utente_esiste, aggiungi_utente, registra_pasto, calcola_livello

TOKEN = "IL_TUO_TOKEN_BOT"

# Inizializza il database
init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    nome = update.message.from_user.first_name

    if not utente_esiste(user_id):
        await update.message.reply_text(f"Ciao {nome}! 👋 Benvenuto nel Food Tracker Bot! 💪\nPer iniziare, inviami i tuoi dati fisici separati da virgola: sesso, età, altezza(cm), peso(kg)\nEsempio: M,16,170,60")
    else:
        await update.message.reply_text(f"Bentornato {nome}! 😎 Scrivi 'oggi: …' per registrare i pasti di oggi o 'ieri: …' se ti sei scordato.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip().lower()

    if not utente_esiste(user_id):
        # onboarding dati utente
        try:
            sesso, eta, altezza, peso = [x.strip() for x in text.split(",")]
            aggiungi_utente(user_id, sesso, int(eta), int(altezza), float(peso))
            await update.message.reply_text("✅ Dati registrati! Ora puoi scrivere 'oggi: …' per registrare i pasti di oggi 🍎🥚")
        except:
            await update.message.reply_text("❌ Formato errato! Riprova: sesso, età, altezza(cm), peso(kg)")
        return

    # Registrazione pasti
    if text.startswith("oggi:") or text.startswith("ieri:"):
        tipo = "oggi" if text.startswith("oggi:") else "ieri"
        contenuto = text.split(":",1)[1].strip()
        registra_pasto(user_id, tipo, contenuto)
        livello = calcola_livello(user_id)
        await update.message.reply_text(f"✅ Ho registrato i tuoi pasti di {tipo}!\n🎯 Livello attuale: {livello} 💪")
    else:
        await update.message.reply_text("Scrivi 'oggi: …' o 'ieri: …' per registrare i pasti 🍎🥚")

# Setup bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
