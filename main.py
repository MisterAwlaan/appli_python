def afficher_menu():
    print("  Menu ")
    print("1-Afficher la liste")
    print("2-Ajout d'un produit")
    print("3-suppression d'un produit")
    print("4-rechercher un produit")
    print("5-Trié le produit par ordre alphabétique")    
    print("6-Quitter")


def afficher_liste():
    with open('./text/liste.txt','r',encoding='utf-8') as liste :
        contenu = liste.read()
        return contenu
    
def ajout_produit():
    nom = input("entrer le nom du produit : ")
    quantite = input("entrer la quantité du produit : ")
    prix = input("entrer le nom du produi : ")
    with open('./text/liste.txt','a',encoding='utf-8') as liste :
        liste.write(f"{nom};{quantite};{prix}\n")
    print(f"Produit'{nom}'ajouté avec succès.")

def suppression_produit():
    afficher_liste()
    produit_a_supprimer = input("Quel produit à supprimer : ")
    with open('./text/liste.txt','r',encoding='utf-8') as liste : 
        produits = liste.readlines()
    produits = [p for p in produits if not p.startswith(produit_a_supprimer+";")]
    with open('./text/liste.txt','w',encoding='utf-8') as liste:
        liste.writelines(produits)
    print(f"Produit'{produit_a_supprimer}'supprimé avec succès") 

    
    pass

def tri_par_ordre_alphabetique():
    with open('./text/liste.txt','r',encoding='utf-8') as liste :
        lignes = liste.readlines()
        tri = sorted([ligne.strip() for ligne in lignes ])
    with open('./text/liste.txt','w') as fichier : 
        for ligne in tri : 
            fichier.write(ligne + '\n')
    

def recherche_produit():
    nom_recherche = input("Entrer le nom du produit : ")
    with open('./text/liste.txt','r',encoding='utf-8') as liste :
        produits = liste.readlines()
    produit_trouve = False
    for produit in produits : 
        nom,quantite,prix = produit.strip().split(';')
        if nom_recherche.lower() in nom.lower():
            print(f"Produit trouvé:Nom:{nom},Quantité:{quantite},Prix:{prix}€")
            produit_trouve = True
        if not produit_trouve:
            print(f"Aucun produit correspond à '{nom_recherche}'trouvé.")
    
    
    
    pass
    
####Script###

afficher_menu()
choix = int(input("Bienvenue dans le menu veuillez choisir votre sélection parmi les 3 propositions : "))

while choix != 6 : 
    
    if choix == 1 : 
        print(afficher_liste())
        print('')
        afficher_menu()
        choix = int(input("Veuillez choisir votre sélection parmi les 3 propositions : "))
    if choix == 2 :
        ajout_produit()
        print('')
        afficher_menu()
        choix = int(input("Veuillez choisir votre sélection parmi les 3 propositions : "))
    if choix == 3: 
        suppression_produit()
        print('')
        afficher_menu()
        choix = int(input("Veuillez choisir votre sélection parmi les 3 propositions : "))
    if choix == 4 : 
        recherche_produit()
        print("")
        choix = int(input("Veuillez choisir votre sélection parmi les 3 propositions : "))
    if choix == 5 : 
        tri_par_ordre_alphabetique()
        print("")
        choix = int(input("Veuillez choisir votre sélection parmi les 3 propositions : "))
    if choix == 6 : 
        print("Aurevoir")
    
