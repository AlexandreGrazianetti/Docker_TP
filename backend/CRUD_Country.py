import mysql.connector
import os

# Récupération des variables d’environnement définies dans docker-compose.yml
MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Country42!")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "country")

# Connexion à la base de données MySQL
try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conn.cursor()
    print("✅ Connexion réussie à MySQL")

    # Création de la table si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pays (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255) UNIQUE NOT NULL,
            population_totale BIGINT NOT NULL,
            capital VARCHAR(255) NOT NULL,
            ville_plus_peuplee VARCHAR(255) NOT NULL,
            population_ville_plus BIGINT NOT NULL,
            ville_moins_peuplee VARCHAR(255) NOT NULL,
            population_ville_moins BIGINT NOT NULL
        )
    """)
    conn.commit()
    print("✅ Table `pays` créée ou déjà existante")

except mysql.connector.Error as err:
    print(f"❌ Erreur MySQL : {err}")

# Fonction pour afficher les pays depuis la base de données
def afficher_tableau_pays():
    cursor.execute("SELECT * FROM pays")
    lignes = cursor.fetchall()

    print("=" * 130)
    print(f"{'Liste des Pays':^130}")
    print("=" * 130)
    print(f"{'Pays':<16} {'Nombre habitants total':<25} {'Capital':<15} {'Ville la plus peuplée':<25} {'Nombre habitants':<20} {'Ville la moins peuplée':<25} {'Nombre habitants':<20}")
    print("-" * 130)

    for ligne in lignes:
        _, pays, nombre_habitants, capital, ville_plus_peuple, nb_habitants_plus, ville_moins_peuple, nb_habitants_moins = ligne
        print(f"{pays:<17}{nombre_habitants:<27}{capital:<16}{ville_plus_peuple:<27}{nb_habitants_plus:<21}{ville_moins_peuple:<27}{nb_habitants_moins:<20}")

    print("=" * 130)

# Menu principal
while True:
    print("\nOptions :")
    print("1. Ajouter un pays")
    print("2. Supprimer un pays")
    print("3. Afficher la liste des pays")
    print("4. Quitter")
    choix = input("Choisissez une option : ")

    if choix == "1":
        # Ajout d'un pays
        nouveau_pays = input("Saisir un pays : ")
        nouveau_nombre_habitants = input("Saisir la population totale du pays saisi : ")
        nouveau_capital = input("Saisir la capitale appartenant au pays : ")
        nouveau_ville_plus_peuple = input("Saisir la ville la plus peuplée qui se situe dans le pays saisi : ")
        nouveau_nombre_habitants_plus = input("Saisir le nombre d'habitants de la ville : ")
        nouveau_ville_moins_peuple = input("Saisir le nom de la ville la moins peuplée qui se situe dans ce même pays : ")
        nouveau_nombre_habitants_moins = input("Saisir le nombre d'habitants de la ville : ")

        try:
            cursor.execute("""
                INSERT INTO pays (nom, population_totale, capital, ville_plus_peuplee, population_ville_plus, ville_moins_peuplee, population_ville_moins)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nouveau_pays, nouveau_nombre_habitants, nouveau_capital, nouveau_ville_plus_peuple, nouveau_nombre_habitants_plus, nouveau_ville_moins_peuple, nouveau_nombre_habitants_moins))
            conn.commit()
            print("✅ Le pays a été ajouté avec succès.")
        except mysql.connector.Error as err:
            print(f"❌ Erreur lors de l'ajout : {err}")

    elif choix == "2":
        # Suppression d'un pays
        supprimer_pays = input("Saisir le nom du pays à supprimer : ")

        try:
            cursor.execute("DELETE FROM pays WHERE nom = %s", (supprimer_pays,))
            conn.commit()
            print("✅ Le pays a été supprimé avec succès.")
        except mysql.connector.Error as err:
            print(f"❌ Erreur lors de la suppression : {err}")

    elif choix == "3":
        # Affichage des pays
        afficher_tableau_pays()

    elif choix == "4":
        print("\n👋 Fermeture du programme...")
        break

    else:
        print("\n❌ Option invalide. Veuillez réessayer.")

# Fermeture de la connexion MySQL
cursor.close()
conn.close()
print("✅ Connexion fermée")
