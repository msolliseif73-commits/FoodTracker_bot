# premium.py
import datetime

premium_users = {}  # user_id -> data scadenza

def attiva_prova(user_id):
    """
    Attiva prova gratuita di 6 giorni
    """
    oggi = datetime.date.today()
    scadenza = oggi + datetime.timedelta(days=6)
    premium_users[user_id] = scadenza
    return scadenza

def is_premium(user_id):
    """
    Controlla se l'utente è premium
    """
    from datetime import date
    if user_id in premium_users:
        if premium_users[user_id] >= date.today():
            return True
    return False
