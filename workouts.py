# workouts.py
def scheda_base(user_dati):
    """
    Restituisce una scheda di allenamento base in base a dati utente
    """
    sesso = user_dati.get("sesso")
    eta = user_dati.get("eta")
    scheda = []

    # Esempio generico
    if eta < 18:
        scheda = [
            "3x10 squat",
            "3x10 push-up",
            "3x30s plank"
        ]
    else:
        scheda = [
            "4x12 squat",
            "4x12 push-up",
            "4x45s plank"
        ]
    return scheda
