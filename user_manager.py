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
        hashed_password = hash_password(password)
        try:
            with open(self.user_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, email, hashed_password])
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
                        return True
            return False
        except FileNotFoundError:
            print("Le fichier utilisateur n'existe pas.")
            return False

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
