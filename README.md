# Fonctionnement global du Projet

Le projet permet d'apporter des modifications, à savoir de lire, d'écrire et de supprimer des lignes au sein d'une base de données qui contient les informations suivantes :
- Nom d'un pays
- Nombre d'habitants du pays
- La capitale
- Nombre d'habitants de la capitale
- Nom de la ville la plus peuplée
- Nombre d'habitants de la ville la plus peuplée
- Nom de la ville la moins peuplée
- Nombre d'habitants de la ville la moins peuplée

## Rôle de chaque conteneur

Le conteneur `backend_service` exécute le code de l'application et permet d'interagir avec le conteneur `db_service` qui lui gère les données via la base de données MySQL.

## Contenu et logique du Dockerfile

Le fichier Dockerfile est composé de différentes commandes, voici une brève explication de chaque commande :
- `FROM python:3.11.9-slim` : Définit l'image utilisée pour générer l'image Docker. Le 'slim' permet de réduire la taille du conteneur.
- `WORKDIR /app` : Détermine le répertoire de travail dans le conteneur. Les commandes après celle-ci seront exécutées dans ce même chemin.
- `COPY requirements.txt .` : Copie le fichier `requirements.txt` vers le répertoire de travail du conteneur.
- `RUN pip install --no-cache-dir -r requirements.txt` : Installe toutes les dépendances nécessaires listées dans le fichier `requirements.txt`. Le paramètre `--no-cache-dir` permet d'éviter de garder des fichiers inutiles, ce qui réduit la taille de l'image Docker.
- `COPY CRUD_Country.py .` : Copie le fichier `CRUD_Country.py` dans le répertoire de travail du conteneur.
- `EXPOSE 5000` : Indique que le conteneur va utiliser le port 5000. Utile pour les scripts Python qui démarrent des serveurs, comme l'API Flask.
- `CMD ["python", "CRUD_Country.py"]` : Exécute le script Python `CRUD_Country.py` via la commande `python`.

## Logique du docker-compose.yml

Le fichier définit 2 services principaux et leurs configurations :
- **backend** : Responsable de l'application backend, à savoir le script `CRUD_Country.py`.
  - `build` : L'application est construite à partir du répertoire nommé `./backend`.
  - `container_name` : Nom du conteneur, `backend_service`.
  - `depends_on` : Cet élément s'adapte au service `db`, il sera donc lancé après le service `db`.
  - `environment` : Variables pour se connecter à la base de données MySQL :
    - `MYSQL_HOST` : L'hôte de la base de données.
    - `MYSQL_USER` : L'identifiant pour accéder à la base.
    - `MYSQL_PASSWORD` : Mot de passe pour se connecter à la base de données.
    - `MYSQL_DATABASE` : Nom de la base de données.
  - `volumes` : Le répertoire local est monté dans le conteneur dans l'emplacement défini, à savoir `./data:/app/data`, ce qui permet de partager des fichiers entre l'hôte et le conteneur.
  - `networks` : Permet la communication avec les autres services.

- **db** : Service responsable de la base de données MySQL.
  - `image` : Image Docker utilisée pour la base de données : `mysql:8`.
  - `container_name` : Nom du conteneur, `db_service`.
  - `restart` : Grâce à `restart: always`, le service redémarre automatiquement en cas d'échec.
  - `environment` : Variables qui configurent la base de données MySQL :
    - `MYSQL_ROOT_PASSWORD` : Mot de passe utilisateur.
    - `MYSQL_USER` : Utilisateur MySQL à créer.
    - `MYSQL_PASSWORD` : Mot de passe lié à l'utilisateur.
    - `MYSQL_DATABASE` : Nom de la base de données à créer.
  - `ports` : Le port utilisé pour MySQL est le 3306, ce qui permet un accès à la base de données en dehors du conteneur.
  - `volumes` : Le volume `db_data` est utilisé pour gérer les données MySQL à l'emplacement défini dans le conteneur.
  - `networks` : Service faisant partie du réseau `my_network`.

Pour la partie Volumes, il n'y a que `db_data` expliquant plus haut. Cela évite les pertes de données dès lors que le conteneur `db` sera supprimé ou redémarré. Pour le Networks, il assure la communication entre les services `backend` et `db` comme hôtes dans les configurations de connexion.

## Guide de lancement

```sh
docker build -t python .
# Commande permettant de construire l'image du conteneur qui se nomme python

docker-compose up -d
# Commande qui lance tous les services définis dans le fichier docker-compose.yml (-d lance les services en mode détaché, c'est-à-dire qu'ils se lancent en arrière-plan).

docker ps
# La commande permet de vérifier les conteneurs qui sont en cours d'exécution.

docker-compose down
# Cette dernière commande permet d'arrêter l'ensemble des conteneurs qui ont été démarrés auparavant.
```

## Explication du code

### Python

Le script principal permet d'appeler plusieurs choses comme :
- L'affichage des pays qui se trouvent dans la table `country`.
- Ajouter de nouveaux pays.
- Supprimer un pays en faisant une recherche via le nom du pays.
- Quitter le programme principal.

### MySQL Workbench

La table `country` contient les informations suivantes :
- `id INT AUTO_INCREMENT PRIMARY KEY`
- `nom VARCHAR(255) UNIQUE NOT NULL` : Noms des pays
- `population_totale BIGINT NOT NULL` : Nombre d'habitants du pays
- `capital VARCHAR(255) NOT NULL` : Leurs capitales
- `population_capitale BIGINT NOT NULL` : Nombre d'habitants de la capitale
- `ville_plus_peuplee VARCHAR(255) NOT NULL` : Nom de la ville la plus peuplée
- `population_ville_plus BIGINT NOT NULL` : Nombre d'habitants de la ville la plus peuplée
- `ville_moins_peuplee VARCHAR(255) NOT NULL` : Nom de la ville la moins peuplée
- `population_ville_moins BIGINT NOT NULL` : Nombre d'habitants de la ville la moins peuplée

### En résumé

Voici les grandes lignes de la logique métier :
- Connexion à la base de données MySQL pour interagir avec les données des pays.
- Opérations CRUD (création, lecture, mise à jour, suppression) sur les informations des pays.
- Validation et gestion des erreurs pour garantir l'intégrité des données et traiter les erreurs.
- Exposition via une API ou une interface backend pour permettre l'accès aux données.

## Optimisation

Enfin, nous pouvons optimiser le fichier grâce à quelques solutions importantes comme un "build multi-stage", ce qui permet de séparer les étapes de construction de l'application. Dans cette approche, les outils et dépendances nécessaires pour la construction (comme `pip`) sont installés dans une première étape, tandis que l'image finale ne contient que les fichiers nécessaires, réduisant ainsi la taille de l'image. Une autre optimisation consiste à utiliser des "images de base plus petites", telles que `python:3.11.9-alpine`, qui est beaucoup plus légère que les versions slim, ce qui permet de réduire davantage la taille de l'image. Cependant, il faut s'assurer que toutes les dépendances fonctionnent bien avec cette version minimale, car certaines peuvent nécessiter des bibliothèques système supplémentaires.

En outre, il est essentiel de "réduire le nombre de couches" en regroupant les commandes `RUN`, `COPY`, et autres dans une seule instruction. Cela diminue le nombre de métadonnées créées et optimise la taille de l'image. Une autre optimisation concerne l'"utilisation du cache Docker". En plaçant les commandes `COPY requirements.txt` avant d’ajouter d’autres fichiers, Docker peut mieux gérer le cache et éviter de réinstaller les dépendances à chaque modification du code, ce qui accélère la construction des images. Ces optimisations combinées permettent non seulement de réduire la taille de l'image, mais aussi d'améliorer les temps de construction et de déploiement.