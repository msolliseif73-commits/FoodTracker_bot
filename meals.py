# meals.py
def aggiungi_pasto(db, user_id, giorno, testo_pasto):
    """
    Inserisce un pasto nel database
    """
    conn = db
    c = conn.cursor()
    c.execute("INSERT INTO pasti (user_id, giorno, contenuto) VALUES (?,?,?)", (user_id, giorno, testo_pasto))
    conn.commit()

def conta_calorie(pasto):
    """
    Esempio base: calcola calorie da testo (da aggiornare con database cibi)
    """
    calorie_totali = 0
    # Se vuoi aggiungere calcolo automatico, qui puoi collegare il tuo database cibi
    return calorie_totali
