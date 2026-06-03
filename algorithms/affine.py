"""Chiffrement affine: C = (a*P + b) mod 26"""


def gcd(a, b):
    """Calcule le PGCD"""
    while b:
        a, b = b, a % b
    return a


def mod_inverse(a, m):
    """Calcule l'inverse modulaire de a modulo m"""
    if gcd(a, m) != 1:
        return None

    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3

    return u1 % m


def is_valid_key(a):
    """Vérifie si 'a' est valide (premier avec 26)"""
    return gcd(a, 26) == 1


def encrypt(text, a, b):
    """Chiffre avec la fonction affine C = (a*P + b) mod 26"""
    if not is_valid_key(a):
        raise ValueError(f"La clé 'a' ({a}) doit être première avec 26")

    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.upper()
            p = ord(char) - 65
            c = (a * p + b) % 26
            encrypted_char = chr(c + 65)
            result += encrypted_char if is_upper else encrypted_char.lower()
        else:
            result += char

    return result


def decrypt(text, a, b):
    """Déchiffre avec P = a^(-1) * (C - b) mod 26"""
    if not is_valid_key(a):
        raise ValueError(f"La clé 'a' ({a}) doit être première avec 26")

    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        raise ValueError(f"Impossible de calculer l'inverse de {a} modulo 26")

    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.upper()
            c = ord(char) - 65
            p = (a_inv * (c - b)) % 26
            decrypted_char = chr(p + 65)
            result += decrypted_char if is_upper else decrypted_char.lower()
        else:
            result += char

    return result


def get_valid_a_values():
    """Retourne les valeurs valides pour 'a'"""
    return [a for a in range(1, 26) if gcd(a, 26) == 1]