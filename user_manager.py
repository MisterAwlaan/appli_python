import csv
import hashlib
import os
import re
from email_util import send_email
from password_utils import hash_password, check_password_strength, is_password_compromised

class UserManager:
    def __init__(self, user_file):
        self.user_file = user_file

    def add_user(self, username, email, password):
        # Vérification de la force du mot de passe
        suggestions = check_password_strength(password)
        if suggestions:
            print("Le mot de passe ne respecte pas les critères de sécurité :")
            for suggestion in suggestions:
                print(suggestion)
            return

        # Vérification si le mot de passe est compromis
        compromised_count = is_password_compromised(password)
        if compromised_count > 0:
            print(f"Le mot de passe a été compromis {compromised_count} fois. Veuillez choisir un autre mot de passe.")
            return

        # Hachage du mot de passe
        hashed_password = hash_password(password)

        # Ajout de l'utilisateur au fichier CSV
        try:
            with open(self.user_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, email, hashed_password])
            print(f"Utilisateur {username} ajouté avec succès.")

            # Envoi d'un e-mail de confirmation
            confirmation_message = f"Bienvenue {username}! Votre compte a été créé avec succès."
            send_email(email, "Confirmation d'inscription", confirmation_message)

            # Vérification et alerte des utilisateurs
            self.verify_and_alert_users()

        except Exception as e:
            print(f"Erreur lors de l'ajout de l'utilisateur : {e}")

    def verify_password(self, password, stored_password):
        try:
            stored_password_bytes = bytes.fromhex(stored_password)
            salt = stored_password_bytes[:16]
            hashed = stored_password_bytes[16:]
            hashed_to_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            return hashed_to_check == hashed
        except ValueError as e:
            print(f"Erreur de conversion hexadécimale : {e}")
            return False


    def login(self, username, password):
        try:
            with open(self.user_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 3:
                        continue
                    if row[0] == username and self.verify_password(password, row[2]):
                        # Vérification de la force du mot de passe
                        suggestions = check_password_strength(password)
                        if suggestions:
                            print("Le mot de passe ne respecte pas les critères de sécurité :")
                            for suggestion in suggestions:
                                print(suggestion)
                            self.verify_and_alert_users()
                        return True
            return False
        except FileNotFoundError:
            print("Le fichier utilisateur n'existe pas.")
            return False

    def modif_password(self, username, old_password, new_password):
        # Vérification de l'ancien mot de passe
        if not self.login(username, old_password):
            print("L'ancien mot de passe est incorrect.")
            return

        # Vérification de la force du nouveau mot de passe
        suggestions = check_password_strength(new_password)
        if suggestions:
            print("Le nouveau mot de passe ne respecte pas les critères de sécurité :")
            for suggestion in suggestions:
                print(suggestion)
            return

        # Vérification si le nouveau mot de passe est compromis
        compromised_count = is_password_compromised(new_password)
        if compromised_count > 0:
            print(f"Le nouveau mot de passe a été compromis {compromised_count} fois. Veuillez choisir un autre mot de passe.")
            return

        # Hachage du nouveau mot de passe
        new_hashed_password = hash_password(new_password)

        # Mise à jour du mot de passe dans le fichier CSV
        try:
            with open(self.user_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)

            with open(self.user_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                for row in rows:
                    if len(row) < 3:
                        continue
                    if row[0] == username:
                        row[2] = new_hashed_password
                    writer.writerow(row)

            print(f"Mot de passe de l'utilisateur {username} modifié avec succès.")

            # Envoi d'un e-mail de confirmation
            confirmation_message = f"Votre mot de passe a été modifié avec succès, {username}."
            send_email(row[1], "Confirmation de modification de mot de passe", confirmation_message)

            # Vérification et alerte des utilisateurs
            self.verify_and_alert_users()

        except Exception as e:
            print(f"Erreur lors de la modification du mot de passe : {e}")
    
    
    
    
    
    
    def verify_and_alert_users(self):
        try:
            with open(self.user_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 3:
                        continue
                    username, email, hashed_password = row
                    if not re.match(r'^[0-9a-fA-F]+$', hashed_password):
                        print(f"Mot de passe haché invalide pour l'utilisateur {username}")
                        continue
                    stored_password_bytes = bytes.fromhex(hashed_password)
                    salt = stored_password_bytes[:16]
                    hashed = stored_password_bytes[16:]
                    compromised_count = is_password_compromised(hashed.hex())
                    if compromised_count > 0:
                        suggestions = check_password_strength(hashed.hex())
                        alert_message = f"Votre mot de passe a été compromis. Voici quelques suggestions pour le renforcer :\n{', '.join(suggestions)}"
                        send_email(email, "Alerte de sécurité", alert_message)
        except FileNotFoundError:
            print("Le fichier utilisateur n'existe pas.")
