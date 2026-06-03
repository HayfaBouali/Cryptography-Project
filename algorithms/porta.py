"""Chiffrement de Porta"""

PORTA_TABLE = {
    'AB': 'NOPQRSTUVWXYZABCDEFGHIJKLM',
    'CD': 'OPQRSTUVWXYZNABCDEFGHIJKLM',
    'EF': 'PQRSTUVWXYZMNABCDEFGHIJKLO',
    'GH': 'QRSTUVWXYZLMNOPABCDEFGHIJK',
    'IJ': 'RSTUVWXYZKLMNOPQABCDEFGHIJ',
    'KL': 'STUVWXYZJKLMNOPQRABCDEFGHI',
    'MN': 'TUVWXYZIJKLMNOPQRSTABCDEFGH',
    'OP': 'UVWXYZGHIJKLMNOPQRSTABCDEF',
    'QR': 'VWXYZFGHIJKLMNOPQRSTABCDE',
    'ST': 'WXYZEFGHIJKLMNOPQRSTUVABCD',
    'UV': 'XYZDEFGHIJKLMNOPQRSTUVWABC',
    'WX': 'YZCDEFGHIJKLMNOPQRSTUVWXAB',
    'YZ': 'ZABCDEFGHIJKLMNOPQRSTUVWXY'
}


def get_row(key_char):
    """Retourne la ligne du tableau"""
    key_char = key_char.upper()
    for keys, row in PORTA_TABLE.items():
        if key_char in keys:
            return row
    return None


def encrypt(text, key):
    """Chiffre avec le chiffre de Porta"""
    if not key or not key.isalpha():
        raise ValueError("La clé doit contenir uniquement des lettres")

    result = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.upper()

            key_char = key[key_index % len(key)]
            row = get_row(key_char)

            if row:
                pos = ord(char) - 65
                encrypted_char = row[pos]
                result += encrypted_char if is_upper else encrypted_char.lower()

            key_index += 1
        else:
            result += char

    return result


def decrypt(text, key):
    """Déchiffre (réciproque)"""
    return encrypt(text, key)