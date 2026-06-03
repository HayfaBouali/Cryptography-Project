"""Chiffrement par transposition"""
import math


def encrypt_columnar(text, key):
    """Transposition columaire simple"""
    text = text.replace(" ", "").upper()
    key = key.upper()
    num_cols = len(key)
    num_rows = math.ceil(len(text) / num_cols)

    text = text.ljust(num_rows * num_cols, 'X')

    grid = []
    idx = 0
    for _ in range(num_rows):
        row = []
        for _ in range(num_cols):
            row.append(text[idx])
            idx += 1
        grid.append(row)

    sorted_indices = sorted(range(num_cols), key=lambda k: key[k])

    result = ""
    for col_idx in sorted_indices:
        for row in grid:
            result += row[col_idx]

    return result


def decrypt_columnar(text, key):
    """Déchiffre une transposition columaire"""
    key = key.upper()
    num_cols = len(key)
    num_rows = len(text) // num_cols

    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    sorted_indices = sorted(range(num_cols), key=lambda k: key[k])

    idx = 0
    for col_idx in sorted_indices:
        for row in range(num_rows):
            grid[row][col_idx] = text[idx]
            idx += 1

    result = ""
    for row in grid:
        result += ''.join(row)

    return result.rstrip('X')


def encrypt_rail_fence(text, rails):
    """Chiffrement Rail Fence (zigzag)"""
    if rails < 2:
        return text

    text = text.replace(" ", "").upper()
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        rail += direction

        if rail == 0 or rail == rails - 1:
            direction = -direction

    return ''.join([''.join(rail) for rail in fence])


def decrypt_rail_fence(text, rails):
    """Déchiffre Rail Fence"""
    if rails < 2:
        return text

    fence = [[] for _ in range(rails)]
    rail_lengths = [0] * rails

    rail = 0
    direction = 1
    for _ in text:
        rail_lengths[rail] += 1
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction

    idx = 0
    for i in range(rails):
        fence[i] = list(text[idx:idx + rail_lengths[i]])
        idx += rail_lengths[i]

    result = []
    rail = 0
    direction = 1
    for _ in text:
        result.append(fence[rail].pop(0))
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction

    return ''.join(result)