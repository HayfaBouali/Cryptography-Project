"""Algorithme RSA"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def generate_keys(bits=2048):
    """Génère une paire de clés RSA"""
    key = RSA.generate(bits)
    private_key = key.export_key().decode()
    public_key = key.publickey().export_key().decode()

    return {
        'private_key': private_key,
        'public_key': public_key,
        'n': key.n,
        'e': key.e,
        'd': key.d
    }


def encrypt(message, public_key):
    """Chiffre avec RSA"""
    try:
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)
        encrypted = cipher.encrypt(message.encode())
        return base64.b64encode(encrypted).decode()
    except Exception as e:
        raise Exception(f"Erreur de chiffrement: {str(e)}")


def decrypt(encrypted_message, private_key):
    """Déchiffre avec RSA"""
    try:
        key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(key)
        decrypted = cipher.decrypt(base64.b64decode(encrypted_message))
        return decrypted.decode()
    except Exception as e:
        raise Exception(f"Erreur de déchiffrement: {str(e)}")