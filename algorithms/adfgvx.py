"""Chiffrement ADFGVX"""
import string

ADFGVX_CHARS = 'ADFGVX'


def create_polybius_square(key):
    """Crée le carré de Polybe 6x6"""
    key = key.upper().replace('J', 'I')
    alphabet = string.ascii_uppercase.replace('J', '') + '0123456789'

    seen = set()
    mixed = []

    for char in key:
        if char in alphabet and char not in seen:
            seen.add(char)
            mixed.append(char)

    for char in alphabet:
        if char not in seen:
            mixed.append(char)

    square = {}
    idx = 0
    for row in ADFGVX_CHARS:
        for col in ADFGVX_CHARS:
            if idx < len(mixed):
                square[mixed[idx]] = row + col
                idx += 1

    return square


def get_reverse_square(square):
    """Inverse le carré de Polybe"""
    return {v: k for k, v in square.items()}


def encrypt(text, keyword_polybius, keyword_transposition):
    """Chiffre avec ADFGVX"""
    square = create_polybius_square(keyword_polybius)

    substituted = ""
    for char in text.upper():
        if char == 'J':
            char = 'I'
        if char in square:
            substituted += square[char]

    keyword_transposition = keyword_transposition.upper()
    num_cols = len(keyword_transposition)

    while len(substituted) % num_cols != 0:
        substituted += 'X'

    num_rows = len(substituted) // num_cols
    grid = []
    idx = 0
    for _ in range(num_rows):
        row = []
        for _ in range(num_cols):
            row.append(substituted[idx])
            idx += 1
        grid.append(row)

    sorted_indices = sorted(range(num_cols), key=lambda k: keyword_transposition[k])

    result = ""
    for col_idx in sorted_indices:
        for row in grid:
            result += row[col_idx]

    return result


def decrypt(text, keyword_polybius, keyword_transposition):
    """Déchiffre avec ADFGVX"""
    keyword_transposition = keyword_transposition.upper()
    num_cols = len(keyword_transposition)
    num_rows = len(text) // num_cols

    sorted_indices = sorted(range(num_cols), key=lambda k: keyword_transposition[k])
    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]

    idx = 0
    for col_idx in sorted_indices:
        for row in range(num_rows):
            grid[row][col_idx] = text[idx]
            idx += 1

    substituted = ""
    for row in grid:
        substituted += ''.join(row)

    square = create_polybius_square(keyword_polybius)
    reverse_square = get_reverse_square(square)

    result = ""
    for i in range(0, len(substituted), 2):
        if i + 1 < len(substituted):
            pair = substituted[i:i + 2]
            if pair in reverse_square:
                result += reverse_square[pair]

    return result.rstrip('X')