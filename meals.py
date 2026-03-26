# meals.py
from database import get_user, update_user_field, add_or_update_user

def handle_meal(update, users_data, file=None):
    user_id = str(update.message.from_user.id)
    text = update.message.text
    user = get_user(user_id) or {}

    # salva pasti
    pasto = {"data": "oggi", "testo": text[5:].strip()}  # puoi migliorare data
    if "pasti" not in user:
        user["pasti"] = []
    user["pasti"].append(pasto)
    
    add_or_update_user(user_id, user)
    update_user_field(user_id, "pasti", user["pasti"])
    
    update.message.reply_text(f"Pasto salvato 🍎: {pasto['testo']}")
