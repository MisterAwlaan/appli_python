def afficher_menu():
    print("  Menu ")
    print("1-Afficher la liste")
    print("2-Ajout d'un produit")
    print("3-suppression d'un produit")

def afficher_liste():
    with open('./text/liste.txt','r',encoding='utf-8') as liste :
        contenu = liste.read()
        return contenu
    
def ajout_produit():
    contenu = input("Nouveau produit : produit:prix   ")
    with open('./text/liste.txt','a') as liste :
        liste.write(contenu + '\n')

def suppression_produit():
    ligne_a_supprimer = input("Entrez la ligne à supprimer (produit:prix) : ")
    
    with open('./text/liste.txt', 'r') as liste:
        lignes = liste.readlines()  
    
    lignes_modifiees = [ligne for ligne in lignes if ligne.strip() != ligne_a_supprimer.strip()]
    with open('./text/liste.txt', 'w') as liste:
        liste.writelines(lignes_modifiees)  

    print("La ligne a été supprimée.")

    
    
    


print(afficher_liste())

