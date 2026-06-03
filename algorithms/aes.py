"""Algorithme AES"""
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


def generate_key(size=256):
    """Génère une clé AES"""
    key_size = size // 8
    return base64.b64encode(get_random_bytes(key_size)).decode()


def encrypt(message, key):
    """Chiffre avec AES-CBC"""
    try:
        try:
            key_bytes = base64.b64decode(key)
        except:
            key_bytes = key.encode()[:32].ljust(32, b'\0')

        iv = get_random_bytes(16)
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)

        padded_message = pad(message.encode(), AES.block_size)
        encrypted = cipher.encrypt(padded_message)

        return base64.b64encode(iv + encrypted).decode()
    except Exception as e:
        raise Exception(f"Erreur de chiffrement: {str(e)}")


def decrypt(encrypted_message, key):
    """Déchiffre avec AES-CBC"""
    try:
        try:
            key_bytes = base64.b64decode(key)
        except:
            key_bytes = key.encode()[:32].ljust(32, b'\0')

        encrypted_data = base64.b64decode(encrypted_message)
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return decrypted.decode()
    except Exception as e:
        raise Exception(f"Erreur de déchiffrement: {str(e)}")