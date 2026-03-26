# levels.py
def calcola_livello(passi_totali):
    """
    Sistema di livelli:
    - Livelli 1-5: 500 passi per livello
    - Livelli 6-15: 500 passi incrementali
    - Dopo livello 15: aumenta di 500 passi per 15 livelli
    - Dopo livello 100: maestrie
    """
    livello = 0
    passi = passi_totali
    # Livelli 1-5
    for i in range(1, 6):
        if passi >= 500:
            passi -= 500
            livello += 1
        else:
            return livello
    # Livelli 6-15
    for i in range(6, 16):
        if passi >= 500:
            passi -= 500
            livello += 1
        else:
            return livello
    # Livelli 16-100
    while livello < 100:
        if passi >= 500:
            passi -= 500
            livello += 1
        else:
            return livello
    # Livelli >100
    while passi >= 1000:
        passi -= 1000
        livello += 1
    return livello
