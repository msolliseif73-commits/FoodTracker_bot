import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
from datetime import date
from utils import emoji_motivazionale, messaggio_bentornato
from meals import aggiungi_pasto, conta_calorie
from levels import calcola_livello
from workouts import scheda_base
from premium import attiva_prova, is_premium

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# --- Database ---
conn = sqlite3.connect('bot.db', check_same_thread=False)
c = conn.cursor()

# Crea tabelle se non esistono
c.execute("""CREATE TABLE IF NOT EXISTS utenti (
    user_id INTEGER PRIMARY KEY,
    nome TEXT,
    sesso TEXT,
    eta INTEGER,
    peso REAL,
    altezza REAL
)""")

c.execute("""CREATE TABLE IF NOT EXISTS pasti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    giorno TEXT,
    contenuto TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS passi (
    user_id INTEGER PRIMARY KEY,
    passi_totali INTEGER DEFAULT 0,
    passi_conservati INTEGER DEFAULT 0
)""")

conn.commit()

# --- Helper ---
def get_user(user_id):
    c.execute("SELECT * FROM utenti WHERE user_id=?", (user_id,))
    return c.fetchone()

def crea_utente(user_id, nome, sesso, eta, peso, altezza):
    c.execute(
        "INSERT OR IGNORE INTO utenti (user_id, nome, sesso, eta, peso, altezza) VALUES (?,?,?,?,?,?)",
        (user_id, nome, sesso, eta, peso, altezza)
    )
    conn.commit()

# --- Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_nome = update.effective_user.first_name
    user = get_user(user_id)
    
    if user:
        await update.message.reply_text(messaggio_bentornato(user_nome))
    else:
        await update.message.reply_text(f"Ciao {user_nome}! Benvenuto nel Food Tracker Bot! {emoji_motivazionale()}")
        await update.message.reply_text("Per iniziare, dimmi il tuo sesso (M/F)")
        context.user_data['stato'] = 'sesso'

async def messaggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    testo = update.message.text.strip()
    stato = context.user_data.get('stato')
    
    if stato == 'sesso':
        context.user_data['sesso'] = testo
        await update.message.reply_text("Quanti anni hai?")
        context.user_data['stato'] = 'eta'
    elif stato == 'eta':
        context.user_data['eta'] = int(testo)
        await update.message.reply_text("Quanto pesi (kg)?")
        context.user_data['stato'] = 'peso'
    elif stato == 'peso':
        context.user_data['peso'] = float(testo)
        await update.message.reply_text("Qual è la tua altezza (cm)?")
        context.user_data['stato'] = 'altezza'
    elif stato == 'altezza':
        context.user_data['altezza'] = float(testo)
        crea_utente(user_id, update.effective_user.first_name,
                    context.user_data['sesso'],
                    context.user_data['eta'],
                    context.user_data['peso'],
                    context.user_data['altezza'])
        await update.message.reply_text("Dati salvati! Ora puoi iniziare a registrare i pasti e i passi!")
        context.user_data['stato'] = None
    else:
        if testo.lower().startswith("oggi:") or testo.lower().startswith("ieri:"):
            giorno = "oggi" if testo.lower().startswith("oggi:") else "ieri"
            contenuto = testo.split(":",1)[1].strip()
            aggiungi_pasto(conn, user_id, giorno, contenuto)
            await update.message.reply_text(f"Pasto registrato per {giorno} {emoji_motivazionale()}")
            
            # Calcolo livello dai passi (se ci sono)
            c.execute("SELECT passi_totali FROM passi WHERE user_id=?", (user_id,))
            res = c.fetchone()
            passi = res[0] if res else 0
            livello = calcola_livello(passi)
            await update.message.reply_text(f"Sei al livello {livello} 💪")
        else:
            await update.message.reply_text("Scrivi 'oggi: <cibo>' o 'ieri: <cibo>' per registrare un pasto.")

# --- Comandi ---
async def passi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    c.execute("SELECT passi_totali, passi_conservati FROM passi WHERE user_id=?", (user_id,))
    res = c.fetchone()
    if not res:
        c.execute("INSERT INTO passi (user_id, passi_totali, passi_conservati) VALUES (?,?,?)", (user_id,0,0))
        conn.commit()
        tot, cons = 0, 0
    else:
        tot, cons = res
    keyboard = [[KeyboardButton("Conserva passi")]]
    await update.message.reply_text(f"Totale passi: {tot}\nPassi conservati: {cons}", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

async def conserva(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    c.execute("SELECT passi_totali, passi_conservati FROM passi WHERE user_id=?", (user_id,))
    res = c.fetchone()
    if res:
        tot, cons = res
        max_conserva = 20000
        spazio = max_conserva - cons
        cons += min(tot, spazio)
        tot -= min(tot, spazio)
        c.execute("UPDATE passi SET passi_totali=?, passi_conservati=? WHERE user_id=?", (tot, cons, user_id))
        conn.commit()
        await update.message.reply_text(f"Passi conservati aggiornati! Totale passi: {tot}, Conservati: {cons}")

async def prova(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    scadenza = attiva_prova(user_id)
    await update.message.reply_text(f"Prova gratuita attivata fino al {scadenza} ✅")

async def scheda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    if user:
        dati = {"sesso": user[2], "eta": user[3]}
        lista = scheda_base(dati)
        await update.message.reply_text("Ecco la tua scheda base:\n" + "\n".join(lista))
    else:
        await update.message.reply_text("Prima devi registrare i tuoi dati con /start")

# --- Setup Application ---
app = ApplicationBuilder().token("<TOKEN>").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("passi", passi))
app.add_handler(CommandHandler("conserva", conserva))
app.add_handler(CommandHandler("prova", prova))
app.add_handler(CommandHandler("scheda", scheda))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messaggi))

print("Bot avviato!")
app.run_polling()
