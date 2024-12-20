from user_manager import UserManager
from product_manager import ProductManager
from utils import get_user_input, get_user_choice

def login_menu():
    user_manager = UserManager('./data/utilisateur.csv')
    product_manager = ProductManager('./data/produits.txt')

    while True:
        print("\nMenu de connexion :")
        print("1. Se connecter")
        print("2. Créer un compte")
        print("3. Quitter")
        choice = get_user_choice("Choisissez une option : ", ['1', '2', '3'])

        if choice == "1":
            username = get_user_input("Nom d'utilisateur : ")
            password = get_user_input("Mot de passe : ")
            if user_manager.login(username, password):
                print(f"Connexion réussie. Bienvenue, {username}!")
                user_menu(username, product_manager)
            else:
                print("Échec de la connexion. Veuillez vérifier vos identifiants.")
        elif choice == "2":
            username = get_user_input("Nom d'utilisateur : ")
            email = get_user_input("Adresse mail : ")
            password = get_user_input("Mot de passe : ")
            try:
                user_manager.add_user(username, email, password)
                user_manager.verify_and_alert_users()
            except Exception as e:
                print(f"Erreur lors de l'inscription : {e}")
        elif choice == "3":
            print("Au revoir")
            break
        else:
            print("Option invalide, veuillez réessayer.")

def user_menu(username, product_manager):
    user_manager = UserManager('./data/utilisateur.csv')
    while True:
        print("\nMenu :")
        print("1. Ajouter un produit")
        print("2. Afficher votre liste")
        print("3. Trier par quantité")
        print("4. Trier par prix")
        print("5. MOdifier mots de passe ")
        choice = get_user_choice("Choisissez une option : ", ['1', '2', '3', '4', '5'])

        if choice == "1":
            product = get_user_input("Entrez le nom du produit à ajouter : ")
            quantity = get_user_input("Entrez la quantité : ")
            price = get_user_input("Entrez le prix à l'unité du produit : ")
            product_manager.add_product(username, product, quantity, price)
            print(f"Produit '{product}' ajouté avec succès à la liste.")
        elif choice == "2":
            product_manager.display_list(username)
        elif choice == "3":
            product_manager.sort_by_quantity()
        elif choice == "4":
            product_manager.sort_by_price()
        elif choice == "5":
            old_password = get_user_input("Entrez l'ancien mot de passe : ")
            new_password = get_user_input("Entrez le nouveau mot de passe : ")
            user_manager.modif_password(username, old_password, new_password)

            
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    login_menu()
