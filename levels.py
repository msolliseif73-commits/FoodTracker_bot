# levels.py
from database import get_user, update_user_field, add_or_update_user

def handle_steps(update, users_data, file=None):
    user_id = str(update.message.from_user.id)
    text = update.message.text
    user = get_user(user_id) or {}

    # estrai passi
    try:
        passi = int(text.split(":")[1].strip())
    except:
        update.message.reply_text("Formato errato! Usa: passi: NUMERO")
        return

    user["passi"] = user.get("passi", 0) + passi

    # calcola livello
    livello = user.get("livello", 0)
    if livello < 5:
        new_level = min(5, user["passi"] // 500)
    elif livello < 100:
        new_level = livello + passi // 500
    else:
        new_level = livello + passi // 1000

    user["livello"] = new_level

    add_or_update_user(user_id, user)
    update.message.reply_text(f"Passi aggiornati 👣: {user['passi']} | Livello: {new_level}")
