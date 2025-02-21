from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = "secret_key"  # Nécessaire pour gérer les sessions

# Récupération des variables d’environnement définies dans docker-compose.yml
MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Country42!")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "country")

# Connexion à la base de données MySQL
def create_connection():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        print("✅ Connexion réussie à MySQL")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Erreur MySQL : {err}")
        return None

# Création de la table si elle n'existe pas
def create_table():
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pays (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255) UNIQUE NOT NULL,
            population_totale BIGINT NOT NULL,
            capital VARCHAR(255) NOT NULL,
            ville_plus_peuplee VARCHAR(255) NOT NULL,
            population_ville_plus            BIGINT NOT NULL,
            ville_moins_peuplee VARCHAR(255) NOT NULL,
            population_ville_moins BIGINT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Table `pays` créée ou déjà existante")

# Appel de la fonction pour créer la table au démarrage de l'application
create_table()

# Route pour afficher la liste des pays et gérer l'ajout d'un nouveau pays
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = create_connection()
    if conn is None:
        return "Erreur de connexion à la base de données", 500

    if request.method == 'POST':
        # Traitement des données du formulaire
        nouveau_pays = request.form.get('pays')
        nouveau_nombre_habitants = request.form.get('nombre_habitants')
        nouveau_capital = request.form.get('capital')
        nouveau_ville_plus_peuple = request.form.get('ville_plus_peuple')
        nouveau_nombre_habitants_plus = request.form.get('nb_habitants_plus')
        nouveau_ville_moins_peuple = request.form.get('ville_moins_peuple')
        nouveau_nombre_habitants_moins = request.form.get('nb_habitants_moins')

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO pays (nom, population_totale, capital, ville_plus_peuplee, population_ville_plus, ville_moins_peuplee, population_ville_moins)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nouveau_pays, nouveau_nombre_habitants, nouveau_capital, nouveau_ville_plus_peuple, nouveau_nombre_habitants_plus, nouveau_ville_moins_peuple, nouveau_nombre_habitants_moins))
            conn.commit()
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            return f"❌ Erreur lors de l'ajout : {err}"
        finally:
            cursor.close()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pays")
    lignes = cursor.fetchall()

    pays_liste = []
    for ligne in lignes:
        pays_liste.append({
            "nom": ligne[1],
            "nombre_habitants": ligne[2],
            "capital": ligne[3],
            "ville_plus_peuple": ligne[4],
            "nb_habitants_plus": ligne[5],
            "ville_moins_peuple": ligne[6],
            "nb_habitants_moins": ligne[7]
        })

    cursor.close()
    conn.close()
    return render_template('pays.html', pays_liste=pays_liste)

# Route pour ajouter un pays via une requête POST
@app.route('/pays', methods=['POST'])
def ajouter_pays():
    data = request.get_json()  # Récupérer les données JSON
    nouveau_pays = data.get('pays')
    nouveau_nombre_habitants = data.get('nombre_habitants')
    nouveau_capital = data.get('capital')
    nouveau_ville_plus_peuple = data.get('ville_plus_peuple')
    nouveau_nombre_habitants_plus = data.get('nb_habitants_plus')
    nouveau_ville_moins_peuple = data.get('ville_moins_peuple')
    nouveau_nombre_habitants_moins = data.get('nb_habitants_moins')

    conn = create_connection()
    if conn is None:
        return jsonify({"message": "Erreur de connexion à la base de données"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO pays (nom, population_totale, capital, ville_plus_peuplee, population_ville_plus, ville_moins_peuplee, population_ville_moins)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nouveau_pays, nouveau_nombre_habitants, nouveau_capital, nouveau_ville_plus_peuple, nouveau_nombre_habitants_plus, nouveau_ville_moins_peuple, nouveau_nombre_habitants_moins))
        conn.commit()
        return jsonify({"message": "Pays ajouté avec succès"}), 201
    except mysql.connector.Error as err:
        return jsonify({"message": f"Erreur lors de l'ajout : {err}"}), 400
    finally:
        cursor.close()
        conn.close()

# Route pour supprimer un pays
@app.route('/pays/<string:nom>', methods=['DELETE'])
def supprimer_pays(nom):
    conn = create_connection()
    if conn is None:
            return jsonify({"message": "Erreur de connexion à la base de données"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pays WHERE nom = %s", (nom,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Aucun pays trouvé avec ce nom"}), 404
        return jsonify({"message": "Pays supprimé avec succès"}), 200
    except mysql.connector.Error as err:
        return jsonify({"message": f"Erreur lors de la suppression : {err}"}), 400
    finally:
        cursor.close()
        conn.close()

# Route pour la déconnexion
@app.route('/deconnexion')
def deconnexion():
    session.clear()
    return redirect(url_for('index'))

# Fermeture de la connexion MySQL lors de l'arrêt de l'application
@app.teardown_appcontext
def fermer_connexion(exception):
    print("✅ Connexion fermée (si elle était ouverte)")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)