# workouts.py
from database import get_user, add_or_update_user

def handle_workout(update, users_data, file=None):
    user_id = str(update.message.from_user.id)
    text = update.message.text
    user = get_user(user_id) or {}

    # salva allenamento
    workout_text = text[12:].strip()  # taglia "allenamento:"
    if "allenamento" not in user:
        user["allenamento"] = []
    user["allenamento"].append({"testo": workout_text})
    
    add_or_update_user(user_id, user)
    
    update.message.reply_text(f"Allenamento salvato 💪: {workout_text}")
