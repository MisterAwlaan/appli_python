import csv
import hashlib
import os

def mots_de_passe_hash(password):
    sel = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), sel, 100000)
    return sel + hashed



def ajouter_utilisateur(username, email, password):
    mots_de_passe_hashe = mots_de_passe_hash(password)

    with open('./text/utilisateur.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, email, mots_de_passe_hashe.hex()])

def verifier_mot_de_passe(password, stored_password):
    stored_password_bytes = bytes.fromhex(stored_password)
    sel = stored_password_bytes[:16]
    hashed = stored_password_bytes[16:]
    hashed_to_check = hashlib.pbkdf2_hmac('sha256', password.encode(), sel, 100000)
    return hashed == hashed_to_check

def connexion(username, password):
    try:
        with open('./text/utilisateur.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
               
                if len(row) < 3:
                    continue
                
                if row[0] == username:
                    
                    if verifier_mot_de_passe(password, row[2]):
                        return True
                    else:
                        return False
        return False  
    except FileNotFoundError:
        print("Le fichier utilisateur n'existe pas.")
        return False



username_input = input("Nom d'utilisateur : ")
password_input = input("Mot de passe : ")

if connexion(username_input, password_input):
    print("Connexion réussie !")
else:
    print("Échec de la connexion.")


