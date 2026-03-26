from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# import dei moduli
from database import get_user, add_or_update_user, update_user_field
from meals import handle_meal
from workouts import handle_workout
from levels import handle_steps

# --- Comandi di base --- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user = get_user(user_id)
    if not user:
        await update.message.reply_text(
            "Ciao! 👋 Prima di iniziare, dimmi qualcosa di te.\n"
            "Formato: sesso, età, altezza(cm), peso(kg)\n"
            "Esempio: M, 16, 163, 55"
        )
    else:
        await update.message.reply_text(
            "Bentornato! 😎\n"
            "Scrivi 'oggi:' per inserire i tuoi pasti 🍎\n"
            "Scrivi 'allenamento:' per la tua scheda 💪\n"
            "Scrivi 'passi:' per aggiornare i passi 👣"
        )

# --- Registrazione nuovo utente --- #
async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    user = get_user(user_id)

    # se utente non esiste, registra i dati base
    if not user:
        try:
            sesso, eta, altezza, peso = [x.strip() for x in text.split(",")]
            add_or_update_user(user_id, {
                "sesso": sesso,
                "eta": int(eta),
                "altezza": int(altezza),
                "peso": int(peso),
                "pasti": [],
                "allenamento": [],
                "passi": 0,
                "livello": 0,
                "conserva_passi": 0
            })
            await update.message.reply_text(
                "Perfetto! ✅ Ora puoi iniziare a tracciare i tuoi pasti, allenamenti e passi."
            )
        except:
            await update.message.reply_text(
                "Formato errato! 😅 Usa: sesso, età, altezza(cm), peso(kg)\nEsempio: M, 16, 163, 55"
            )

# --- Handler messaggi --- #
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if text.startswith("oggi:") or text.startswith("ieri:"):
        handle_meal(update, None)
    elif text.startswith("allenamento:"):
        handle_workout(update, None)
    elif text.startswith("passi:"):
        handle_steps(update, None)
    else:
        await update.message.reply_text(
            "Non ho capito 😅\nUsa 'oggi:', 'ieri:', 'allenamento:' o 'passi:'"
        )

# --- Avvio bot --- #
if __name__ == "__main__":
    app = ApplicationBuilder().token("IL_TUO_TOKEN_DEL_BOT").build()
    
    # comandi
    app.add_handler(CommandHandler("start", start))
    
    # messaggi utente
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), register_user))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    
    print("🚀 Bot avviato e live!")
    app.run_polling()
