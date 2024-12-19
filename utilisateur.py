import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import csv
import requests
import hashlib
import os

# Configuration de l'email
EMAIL_FROM = "nidri@guardiaschool.fr"
EMAIL_PASSWORD = "votre_mot_de_passe_d_application"  # Remplacez par votre mot de passe d'application

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

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        server.quit()
    except smtplib.SMTPAuthenticationError as e:
        print(f"Erreur d'authentification SMTP : {e}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")

def is_password_compromised(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1_password[:5], sha1_password[5:]
    response = requests.get(f'https://api.pwnedpasswords.com/range/{first5_char}')
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == tail:
            return int(count)
    return 0

def verify_and_alert_users():
    try:
        with open('./text/utilisateur.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 3:
                    continue
                username, email, hashed_password = row
                if not re.match(r'^[0-9a-fA-F]+$', hashed_password):
                    print(f"Mot de passe haché invalide pour l'utilisateur {username}")
                    continue
                stored_password_bytes = bytes.fromhex(hashed_password)
                salt = stored_password_bytes[:32]
                hashed = stored_password_bytes[32:]
                compromised_count = is_password_compromised(hashed.hex())
                if compromised_count > 0:
                    suggestions = check_password_strength(hashed.hex())
                    alert_message = f"Votre mot de passe a été compromis. Voici quelques suggestions pour le renforcer :\n{', '.join(suggestions)}"
                    send_email(email, "Alerte de sécurité", alert_message)
    except FileNotFoundError:
        print("Le fichier utilisateur n'existe pas.")

def login_menu():
    while True:
        print("\nMenu de connexion :")
        print("1. Se connecter")
        print("2. Créer un compte")
        print("3. Quitter")
        choice = input("Choisissez une option : ")

        if choice == "1":
            username = input("Nom d'utilisateur : ")
            password = input("Mot de passe : ")
            if login(username, password):
                print(f"Connexion réussie. Bienvenue, {username}!")
                user_menu(username)
            else:
                print("Échec de la connexion. Veuillez vérifier vos identifiants.")
        elif choice == "2":
            username = input("Nom d'utilisateur : ")
            email = input("Adresse mail : ")
            password = input("Mot de passe : ")
            try:
                add_user(username, email, password)
                verify_and_alert_users()
            except Exception as e:
                print(f"Erreur lors de l'inscription : {e}")
        elif choice == "3":
            print("Au revoir")
            break
        else:
            print("Option invalide, veuillez réessayer.")

def add_user(username, email, password):
    hashed_password = hash_password(password)
    try:
        with open('./text/utilisateur.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, email, hashed_password])
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'utilisateur : {e}")

def verify_password(password, stored_password):
    try:
        stored_password_bytes = bytes.fromhex(stored_password)
        salt = stored_password_bytes[:32]
        hashed = stored_password_bytes[32:]
        hashed_to_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return hashed_to_check == hashed
    except ValueError as e:
        print(f"Erreur de conversion hexadécimale : {e}")
        return False

def login(username, password):
    try:
        with open('./text/utilisateur.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 3:
                    continue
                if row[0] == username and verify_password(password, row[2]):
                    return True
        return False
    except FileNotFoundError:
        print("Le fichier utilisateur n'existe pas.")
        return False

def user_menu(username):
    while True:
        print("\nMenu :")
        print("1. Ajouter un produit")
        print("2. Afficher votre liste")
        print("3. Se déconnecter")
        choice = input("Choisissez une option : ")

        if choice == "1":
            product = input("Entrez le nom du produit à ajouter : ")
            quantity = input("Entrez la quantité : ")
            price = input("Entrez le prix à l'unité du produit : ")
            add_product(username, product, quantity, price)
            print(f"Produit '{product}' ajouté avec succès à la liste.")
        elif choice == "2":
            display_list(username)
        elif choice == "3":
            login_menu()
        else:
            print("Option invalide, veuillez réessayer.")

def add_product(username, product, quantity, price):
    with open('./text/produits.txt', mode='a') as file:
        file.write(f"{username}, {product},{quantity},{price}\n")

def display_list(username):
    try:
        with open('./text/produits.txt', 'r') as file:
            products = [line.strip().split(',') for line in file if line.startswith(username + ",")]

        if products:
            print("\nVotre liste de produits :")
            print(f"{'Produit':<20} {'Quantité':<10} {'Prix unitaire':<15}")
            for product in products:
                print(f"{product[1]:<20} {product[2]:<10} {product[3]:<15}")
        else:
            print("Aucun produit trouvé dans votre liste.")
    except FileNotFoundError:
        print("Le fichier de produits est introuvable.")

def sort_by_quantity():
    with open('./text/liste.txt', 'r') as file:
        lines = file.readlines()
    for i in range(1, len(lines)):
        current_line = lines[i]
        current_quantity = float(current_line.strip().split(';')[1])
        j = i - 1

        while j >= 0 and float(lines[j].strip().split(';')[1]) > current_quantity:
            lines[j + 1] = lines[j]
            j -= 1

        lines[j + 1] = current_line

    with open('./text/liste.txt', 'w') as file:
        for line in lines:
            file.write(line.strip() + '\n')

    print("Le tri par quantité a été effectué.")

def quicksort_by_price(lines):
    if len(lines) <= 1:
        return lines
    pivot = float(lines[-1].strip().split(';')[2])

    less_than_pivot = [line for line in lines[:-1] if float(line.strip().split(';')[2]) <= pivot]
    greater_than_pivot = [line for line in lines[:-1] if float(line.strip().split(';')[2]) > pivot]

    return quicksort_by_price(less_than_pivot) + [lines[-1]] + quicksort_by_price(greater_than_pivot)

def sort_by_price():
    with open('./text/liste.txt', 'r') as file:
        lines = file.readlines()

    sorted_lines = quicksort_by_price(lines)
    with open('./text/liste.txt', 'w') as file:
        for line in sorted_lines:
            file.write(line.strip() + '\n')

    print("Le tri par prix avec QuickSort a été effectué.")

### Script ###
login_menu()
