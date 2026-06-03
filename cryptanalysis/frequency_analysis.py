"""Analyse de fréquence pour la cryptanalyse"""
from collections import Counter
import string

# Fréquences moyennes en français
FRENCH_FREQ = {
    'E': 14.7, 'A': 7.6, 'I': 7.5, 'S': 7.9, 'N': 7.1,
    'R': 6.6, 'T': 7.2, 'O': 5.8, 'L': 5.5, 'U': 6.3,
    'D': 3.7, 'C': 3.2, 'M': 3.0, 'P': 3.0, 'G': 1.2,
    'B': 1.1, 'V': 1.6, 'H': 1.1, 'F': 1.1, 'Q': 0.7,
    'Y': 0.4, 'X': 0.4, 'J': 0.3, 'K': 0.1, 'W': 0.1, 'Z': 0.1
}


def analyze_frequency(text):
    """Analyse la fréquence des lettres"""
    # Filtrer seulement les lettres
    letters = [c.upper() for c in text if c.isalpha()]
    total = len(letters)

    if total == 0:
        return {}

    # Compter les occurrences
    counter = Counter(letters)

    # Calculer les pourcentages
    frequencies = {letter: (count / total) * 100
                   for letter, count in counter.items()}

    # Ajouter les lettres manquantes avec 0%
    for letter in string.ascii_uppercase:
        if letter not in frequencies:
            frequencies[letter] = 0.0

    return dict(sorted(frequencies.items()))


def get_most_common(text, n=5):
    """Retourne les n lettres les plus fréquentes"""
    freq = analyze_frequency(text)
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:n]


def chi_squared_test(text):
    """Test du chi-carré pour détecter le décalage César"""
    best_shift = 0
    min_chi = float('inf')

    for shift in range(26):
        from algorithms.caesar import decrypt
        decrypted = decrypt(text, shift)
        freq = analyze_frequency(decrypted)

        chi = 0
        for letter in string.ascii_uppercase:
            expected = FRENCH_FREQ.get(letter, 0)
            observed = freq.get(letter, 0)
            if expected > 0:
                chi += ((observed - expected) ** 2) / expected

        if chi < min_chi:
            min_chi = chi
            best_shift = shift

    return best_shift, min_chi