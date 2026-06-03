"""Algorithme de chiffrement César"""


def encrypt(text, shift):
    """Chiffre le texte avec le décalage donné"""
    result = ""
    shift = shift % 26

    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result


def decrypt(text, shift):
    """Déchiffre le texte"""
    return encrypt(text, -shift)


def brute_force(ciphertext):
    """Retourne tous les déchiffrements possibles"""
    results = []
    for shift in range(26):
        decrypted = decrypt(ciphertext, shift)
        results.append((shift, decrypted))
    return results