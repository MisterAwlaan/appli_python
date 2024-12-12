import csv
import hashlib
import os

def mots_de_passe_hash(password):
    sel = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), sel, 100000)
    return sel + hashed

def veri_mots_de_passe(mots_de_passe_stocke, provided_password):
    sel = mots_de_passe_stocke[:16]  # Extrait le sel des 16 premiers bytes
    hash_stocke = mots_de_passe_stocke[16:]  # Le reste est le hachage
    provided_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), sel, 100000)
    return hash_stocke == provided_hash

def ajouter_utilisateur(username, email, password):
    mots_de_passe_hashe = mots_de_passe_hash(password)

    with open('./text/utilisateur.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, email, mots_de_passe_hashe.hex()])

def connexion(username, password):
    with open('./text/utilisateur.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                mots_de_passe_stocke = bytes.fromhex(row[2])
                if veri_mots_de_passe(mots_de_passe_stocke, password):
                    return True
    return False

# Exemple d'utilisation
username = 'test'
password = 'test'

if connexion(username, password):
    print("Connexion réussie !")
else:
    print("Nom d'utilisateur ou mot de passe incorrect.")
