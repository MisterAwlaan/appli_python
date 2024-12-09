
### Menu ###
def afficher_liste():
    liste = open("liste.txt","r",encoding="utf8")
    line = liste.read()
    return line

print(afficher_liste())