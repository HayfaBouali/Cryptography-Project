"""Chiffrement par substitution avec alphabets désordonnés"""
import random
import string


def generate_random_alphabet():
    """Génère un alphabet désordonné aléatoirement"""
    alphabet = list(string.ascii_uppercase)
    random.shuffle(alphabet)
    return ''.join(alphabet)


def generate_keyword_alphabet(keyword):
    """Génère un alphabet désordonné horizontal"""
    keyword = keyword.upper()
    seen = set()
    key_letters = []
    for char in keyword:
        if char.isalpha() and char not in seen:
            seen.add(char)
            key_letters.append(char)

    for char in string.ascii_uppercase:
        if char not in seen:
            key_letters.append(char)

    return ''.join(key_letters)


def generate_vertical_alphabet(keyword, cols=5):
    """Génère un alphabet désordonné vertical"""
    keyword = keyword.upper()
    seen = set()
    key_letters = []
    for char in keyword:
        if char.isalpha() and char not in seen:
            seen.add(char)
            key_letters.append(char)

    rows = (26 + cols - 1) // cols
    grid = [['' for _ in range(cols)] for _ in range(rows)]

    idx = 0
    for col in range(cols):
        for row in range(rows):
            if idx < len(key_letters):
                grid[row][col] = key_letters[idx]
                idx += 1
            else:
                break

    remaining = [c for c in string.ascii_uppercase if c not in seen]
    for char in remaining:
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '':
                    grid[row][col] = char
                    break
            else:
                continue
            break

    result = []
    for row in grid:
        result.extend([c for c in row if c])

    return ''.join(result[:26])


def encrypt(text, substitution_alphabet):
    """Chiffre avec un alphabet de substitution"""
    if len(substitution_alphabet) != 26:
        raise ValueError("L'alphabet doit contenir 26 lettres")

    normal_alphabet = string.ascii_uppercase
    trans_table = str.maketrans(normal_alphabet, substitution_alphabet.upper())

    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            encrypted = char.upper().translate(trans_table)
            result += encrypted if is_upper else encrypted.lower()
        else:
            result += char

    return result


def decrypt(text, substitution_alphabet):
    """Déchiffre"""
    if len(substitution_alphabet) != 26:
        raise ValueError("L'alphabet doit contenir 26 lettres")

    normal_alphabet = string.ascii_uppercase
    trans_table = str.maketrans(substitution_alphabet.upper(), normal_alphabet)

    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            decrypted = char.upper().translate(trans_table)
            result += decrypted if is_upper else decrypted.lower()
        else:
            result += char

    return result