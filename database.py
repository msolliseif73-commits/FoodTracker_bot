# database.py
import sqlite3

DB_NAME = "foodtracker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # tabella utenti
    c.execute("""CREATE TABLE IF NOT EXISTS utenti (
                    user_id INTEGER PRIMARY KEY,
                    sesso TEXT,
                    eta INTEGER,
                    altezza INTEGER,
                    peso REAL
                )""")
    # tabella pasti
    c.execute("""CREATE TABLE IF NOT EXISTS pasti (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    giorno TEXT,
                    contenuto TEXT
                )""")
    conn.commit()
    conn.close()

def utente_esiste(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM utenti WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def aggiungi_utente(user_id, sesso, eta, altezza, peso):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO utenti VALUES (?,?,?,?,?)", (user_id, sesso, eta, altezza, peso))
    conn.commit()
    conn.close()

def registra_pasto(user_id, giorno, contenuto):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO pasti (user_id, giorno, contenuto) VALUES (?,?,?)", (user_id, giorno, contenuto))
    conn.commit()
    conn.close()

def calcola_livello(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM pasti WHERE user_id=?", (user_id,))
    count = c.fetchone()[0]
    conn.close()
    # esempio: 1 livello ogni 3 pasti registrati
    livello = 1 + count // 3
    return livello
