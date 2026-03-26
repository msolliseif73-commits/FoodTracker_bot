import json
from pathlib import Path

DB_FILE = "users.json"

# --- Funzioni principali --- #

def load_users():
    """Legge tutto il database dal file JSON"""
    if Path(DB_FILE).exists():
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(data):
    """Salva tutto il database nel file JSON"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_user(user_id):
    """Restituisce i dati di un singolo utente, o None se non esiste"""
    users = load_users()
    return users.get(str(user_id))

def add_or_update_user(user_id, user_data):
    """Aggiunge un nuovo utente o aggiorna i dati esistenti"""
    users = load_users()
    users[str(user_id)] = user_data
    save_users(users)

def update_user_field(user_id, field, value):
    """Aggiorna un singolo campo dell’utente"""
    users = load_users()
    user = users.get(str(user_id), {})
    user[field] = value
    users[str(user_id)] = user
    save_users(users)
