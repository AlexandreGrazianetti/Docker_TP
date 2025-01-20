import csv

# Saisie des informations concernant la nouvelle ville à ajouter.
nouveau_pays = input("Saisir un pays : ")
nouveau_nombre_habitants = input("Saisir la population totale du pays saisi : ")
nouveau_Capital = input("Saisir la capitale appartenant au pays : ")
nouveau_Ville_plus_peuple = input("Saisir la ville la plus peuplée qui se situe dans le pays saisi : ")
nouveau_Nombre_Habitants_Ville_Plus = input("Saisir le nombre d'habitants de la ville : ")
nouveau_Ville_moins_peuple = input("Saisir le nom de la ville la moins peuplée qui se situe dans ce même pays : ")
nouveau_Nombre_Habitants_Ville_Moins = input("Saisir le nombre d'habitants de la ville : ")

# Enchaînement des processus permettant d'écrire dans le fichier
with open('pays.csv', 'a', newline='') as fichier_csv_sortie:
    enregistreur_csv = csv.writer(fichier_csv_sortie)
    enregistreur_csv.writerow([
        nouveau_pays,
        nouveau_nombre_habitants,
        nouveau_Capital,
        nouveau_Ville_plus_peuple,
        nouveau_Nombre_Habitants_Ville_Plus,
        nouveau_Ville_moins_peuple,
        nouveau_Nombre_Habitants_Ville_Moins
    ])

# Affichage de la liste des pays
print("=" * 130)
print(f"{'Liste des Pays':^130}")
print("=" * 130)
print(f"{'Pays':<16} {'Nombre habitants total':<25} {'Capital':<15} {'Ville la plus peuplée':<25} {'Nombre habitants':<20} {'Ville la moins peuplée':<25} {'Nombre habitants':<20}")
print("-" * 130)
# Lecture et affichage du contenu du fichier CSV
with open('pays.csv', 'r') as fichier_csv:
    lecteur_csv = csv.reader(fichier_csv, delimiter=',')
    next(lecteur_csv)  # Sauter la première ligne (en-têtes)
    for ligne in lecteur_csv:
        if len(ligne) == 7:  # Vérifier que la ligne a exactement 7 colonnes
            pays = ligne[0]
            nombre_habitants = ligne[1]
            Capital = ligne[2]
            Ville_plus_peuple = ligne[3]
            Nombre_Habitants_Ville_Plus = ligne[4]
            Ville_moins_peuple = ligne[5]
            Nombre_Habitants_Ville_Moins = ligne[6]
            # Affichage de chaque ligne du fichier
            print(f"{pays:<17}{nombre_habitants:<27}{Capital:<16}{Ville_plus_peuple:<27}{Nombre_Habitants_Ville_Plus:<21}{Ville_moins_peuple:<27}{Nombre_Habitants_Ville_Moins:<20}")
