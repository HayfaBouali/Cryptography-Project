"""Algorithme de chiffrement Vigenère"""


def encrypt(text, key):
    """Chiffre le texte avec la clé de Vigenère"""
    result = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            shift = ord(key[key_index % len(key)]) - 65
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            key_index += 1
        else:
            result += char
    return result


def decrypt(text, key):
    """Déchiffre le texte"""
    result = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            shift = ord(key[key_index % len(key)]) - 65
            result += chr((ord(char) - shift_base - shift) % 26 + shift_base)
            key_index += 1
        else:
            result += char
    return result