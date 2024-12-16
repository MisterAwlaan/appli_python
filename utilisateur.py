import csv
import hashlib
import os

def mots_de_passe_hash(password):
    sel = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), sel, 100000)
    return sel + hashed

def menu_connexion():
    
    while True :
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
            
        elif choix == "3":
            print("aurevoir")
            break
        
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
        print("2. Afficher votre liste")
        print("3. Se déconnecter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            produit = input("Entrez le nom du produit à ajouter : ")
            quantite = input("entrer la quantité : ")
            prix = input("entrer le prix à l'unité du produit : ")
            ajouter_produit(username, produit , quantite , prix)
            print(f"Produit '{produit}' ajouté avec succès à la liste.")
        elif choix == "2":
            afficher_liste(username)
            break
        else:
            print("Option invalide, veuillez réessayer.")

def ajouter_produit(username,produit,quantite , prix):
    with open('./text/produits.txt', mode='a') as file:
        file.write(f"{username}, {produit},{quantite},{prix}\n")

def afficher_liste(username):
    try:
        with open('./text/produits.txt', 'r') as file:
            produits = [line.strip().split(',') for line in file if line.startswith(username + ",")]

        if produits:
            print("\nVotre liste de produits :")
            print(f"{'Produit':<20} {'Quantité':<10} {'Prix unitaire':<15}")
            for produit in produits:
                print(f"{produit[1]:<20} {produit[2]:<10} {produit[3]:<15}")
        else:
            print("Aucun produit trouvé dans votre liste.")
    except FileNotFoundError:
        print("Le fichier de produits est introuvable.")




def tri_par_quantite():
    with open('./text/liste.txt', 'r') as liste:
        lignes = liste.readlines()
    for i in range(1, len(lignes)):
        
        current_line = lignes[i]
        current_quantity = float(current_line.strip().split(';')[1])
        j = i - 1
        
        
        while j >= 0 and float(lignes[j].strip().split(';')[1]) > current_quantity:
            lignes[j + 1] = lignes[j]
            j -= 1
        
        
        lignes[j + 1] = current_line

    
    with open('./text/liste.txt', 'w') as liste:
        for ligne in lignes:
            liste.write(ligne.strip() + '\n')
    
    print("Le tri par quantité a été effectué.")


def quicksort_prix(lignes):
    if len(lignes) <= 1:
        return lignes  
    pivot = float(lignes[-1].strip().split(';')[2])
    
    moins_que_pivot = [ligne for ligne in lignes[:-1] if float(ligne.strip().split(';')[2]) <= pivot]
    plus_que_pivot = [ligne for ligne in lignes[:-1] if float(ligne.strip().split(';')[2]) > pivot]

    return quicksort_prix(moins_que_pivot) + [lignes[-1]] + quicksort_prix(plus_que_pivot)


def tri_par_prix():
    with open('./text/liste.txt', 'r') as liste:
        lignes = liste.readlines()

    
    lignes_triees = quicksort_prix(lignes)
    with open('./text/liste.txt', 'w') as fichier:
        for ligne in lignes_triees:
            fichier.write(ligne.strip() + '\n')
    
    print("Le tri par prix avec QuickSort a été effectué.")


### script ###


menu_connexion()