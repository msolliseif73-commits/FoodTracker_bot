from database import get_user, add_or_update_user, update_user_field

user_id = update.message.from_user.id

# Controllo se l’utente esiste
user = get_user(user_id)
if not user:
    # aggiungo nuovo utente
    add_or_update_user(user_id, {"sesso": "M", "eta": 16, "altezza": 163, "peso": 55})
else:
    # aggiorno un campo
    update_user_field(user_id, "passi", 3000)
