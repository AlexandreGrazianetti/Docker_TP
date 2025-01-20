import csv

#Saisi des informations concernant la nouvelle ville à ajouter.
nouveau_pays = input("Saisir un pays :")
nouveau_nombre_habitants = input("Saisir la population totale du pays saisi :")
nouveau_Capital = input("Saisir la capitale appartenant au pays :")
nouveau_Ville_plus_peuple = input("Saisir la ville la plus peuplé qui se situe dans la pays saisi :")
nouveau_Nombre_Habitants_Ville_Plus = input("Saisir le nombre d'habitants de la ville :")
nouveau_Ville_moins_peuple = input("Saisir le nom de la ville la moins peuplé qui se situe dans ce même pays :")
nouveau_Nombre_Habitants_Ville_Moins = input("Saisir le nombre d'habitants de la ville :")

print("Liste des Pays")
print('-'*57)
print(f"{'Pays':<16} {'Nombre habitants total':<25} {'Capital':<15} {'Ville la plus peuplée':<25} {'Nombre habitants':<20} {'Ville la moins peuplée':<25} {'Nombre habitants':<20}")
voyelles = list("aeiouyAEIOUY")

#Enchaînement des processus permettant de lire et d'écrire dans ce fichier
with open('pays.csv') as fichier_csv:
    lecteur_csv = csv.reader(fichier_csv, delimiter=',')
    with open('pays.csv', 'w', newline='') as fichier_csv_sortie:
        enregistreur_csv = csv.writer(fichier_csv_sortie)
        # Sauter la première ligne (les en-têtes)
        next(lecteur_csv)

        nombre_lignes = 0
        for ligne in lecteur_csv:
            pays = ligne[0]
            nombre_habitants = ligne[1]
            Capital = ligne[2]
            Ville_plus_peuple = ligne[3]
            Nombre_Habitants_Ville_Plus = ligne[4]
            Ville_moins_peuple = ligne[5]
            Nombre_Habitants_Ville_Moins = ligne[6]
            if pays[0] in voyelles :
                enregistreur_csv.writerow( [ ligne[0], ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6] ] )                
            nombre_lignes += 1
            #Affichage du nouveau tableau avec ou sans les informations saisi.
            print(f"{pays:<17}{nombre_habitants:<27}{Capital:<16}{Ville_plus_peuple:<27}{Nombre_Habitants_Ville_Plus:<21}{Ville_moins_peuple:<27}{Nombre_Habitants_Ville_Moins:<20}")