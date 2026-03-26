from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
from utils import load_users, save_users
from meals import handle_meal
from workouts import handle_workout
from levels import handle_steps

USERS_FILE = "users.json"
users_data = load_users(USERS_FILE)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if user_id not in users_data:
        await update.message.reply_text(
            "Ciao! 👋 Prima di iniziare, dimmi qualcosa di te.\n"
            "Formato: sesso, età, altezza(cm), peso(kg)\n"
            "Esempio: M, 16, 163, 55"
        )
    else:
        await update.message.reply_text("Bentornato! Scrivi 'oggi:' per inserire i tuoi pasti 🍎")

async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    text = update.message.text
    try:
        sesso, eta, altezza, peso = [x.strip() for x in text.split(",")]
        users_data[user_id] = {"sesso": sesso, "eta": int(eta), "altezza": int(altezza), "peso": int(peso)}
        save_users(USERS_FILE, users_data)
        await update.message.reply_text("Perfetto! ✅ Ora puoi iniziare a tracciare i tuoi pasti e allenamenti.")
    except:
        await update.message.reply_text("Formato errato! Usa: sesso, età, altezza(cm), peso(kg)")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)
    
    if text.lower().startswith("oggi:") or text.lower().startswith("ieri:"):
        await handle_meal(update, users_data, USERS_FILE)
    elif text.lower().startswith("allenamento:"):
        await handle_workout(update, users_data, USERS_FILE)
    elif text.lower().startswith("passi:"):
        await handle_steps(update, users_data, USERS_FILE)
    else:
        await update.message.reply_text("Non ho capito 😅. Usa 'oggi:', 'ieri:', 'allenamento:' o 'passi:'")

if __name__ == "__main__":
    app = ApplicationBuilder().token("IL_TUO_TOKEN_DEL_BOT").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), register_user))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    
    print("🚀 Bot avviato e live!")
    app.run_polling()
