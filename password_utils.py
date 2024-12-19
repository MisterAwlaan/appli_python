import hashlib
import os
import re
import requests

def hash_password(password):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + hashed.hex()

def check_password_strength(password):
    suggestions = []
    if len(password) < 12:
        suggestions.append("Le mot de passe doit contenir au moins 12 caractères.")
    if not re.search(r'[A-Z]', password):
        suggestions.append("Le mot de passe doit contenir au moins une lettre majuscule.")
    if not re.search(r'[a-z]', password):
        suggestions.append("Le mot de passe doit contenir au moins une lettre minuscule.")
    if not re.search(r'[0-9]', password):
        suggestions.append("Le mot de passe doit contenir au moins un chiffre.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        suggestions.append("Le mot de passe doit contenir au moins un caractère spécial.")
    return suggestions

def is_password_compromised(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1_password[:5], sha1_password[5:]
    response = requests.get(f'https://api.pwnedpasswords.com/range/{first5_char}')
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == tail:
            return int(count)
    return 0
