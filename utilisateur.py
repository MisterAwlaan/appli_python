import csv
import hashlib
import os

def mots_de_passe_hash(password):
    sel = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), sel, 100000)
    return sel + hashed

def menu_connexion():
    while True:
        print("\nMenu de connexion :")
        print("1. Se connecter")
        print("2. Créer un compte")
        print("3. Quitter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            username = input("Nom d'utilisateur : ")
            password = input("Mot de passe : ")
            utilisateur_connecte = connexion(username, password)

            if utilisateur_connecte:
                print(f"Connexion réussie. Bienvenue, {utilisateur_connecte}!")
                menu_utilisateur(utilisateur_connecte)
            else:
                print("Échec de la connexion. Veuillez vérifier vos identifiants.")
        elif choix == "2":
            username = input("Nom d'utilisateur : ")
            email = input("adresse mail : ")
            password = input("Mot de passe : ")
            ajouter_utilisateur(username,email,password)
            
        else:
            print("Option invalide, veuillez réessayer.")


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
                        return username
                    else:
                        return False
        return False  
    except FileNotFoundError:
        print("Le fichier utilisateur n'existe pas.")
        return False

def menu_utilisateur(username):
    while True:
        print("\nMenu :")
        print("1. Ajouter un produit")
        print("2. Se déconnecter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            produit = input("Entrez le nom du produit à ajouter : ")
            quantite = input("entrer la quantité : ")
            prix = input("entrer le prix à l'unité du produit : ")
            ajouter_produit(username, produit , quantite , prix)
            print(f"Produit '{produit}' ajouté avec succès à la liste.")
        elif choix == "2":
            print("Déconnexion réussie.")
            break
        else:
            print("Option invalide, veuillez réessayer.")

def ajouter_produit(username,produit,quantite , prix):
    with open('./text/produits.txt', mode='a') as file:
        file.write(f"{username}, {produit},{quantite},{prix}\n")


### script ###


menu_connexion()