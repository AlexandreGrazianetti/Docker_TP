Fonctionnement global du Projet :
 Le projet permet d'apporter des modifications, à savoir de lire, d'écrire et de supprimer des lignes au sein d'une base de données qui contient les informations suivantes :
    - Nom d'un pays
    - Nombre d'habitants du pays
    - La capitale
    - Nombre d'habitants de la capitale
    - Nom de la ville la plus peuplé
    - Nombre d'habitants de la ville la plus peuplé
    - Nom de la ville la moins peuplé
    - Nombre d'habitants de la ville la plus moins

Rôle de chaque conteneur :
Le conteneur 'backend_service' exécute le code de l'application et permet d'interargir avec le conteneur db_service qui lui gère les données via la base de donnée MYSQL.

Contenu et logique du DockerFile :
Le fichier Dockerfile est composé de différentes commandes, voici une brève explication de chaque commande :
    # Définit l'image utilisé pour générer l'image Docker. A savoir que le 'slim' permet de réduire la taille du conteneur.
    FROM python:3.11.9-slim  
    # Détermine le répertoire de travail dans le conteneur. Ce qui veut dire que les commandes après celle-ci seront exécutés dans ce même chemin.
    WORKDIR /app
    # La commande permet de copier le fichier cités ci-dessous et de le déposer vers le répertoire de travail du conteneur.
    COPY requirements.txt .  
    # Elle exécute la commande pour installer toutes les dépendances nécessaire et listés dans le fichier requirements.txt.
    # Le paramètre --no-cache-dir permet d'éviter de garder des fichiers inutiles, ce qui réduit la taille de l'image Docker.
    RUN pip install --no-cache-dir -r requirements.txt  
    # Comme la commande COPY requirements.txt, elle copie le fichier défini et le dépose dans la zone de travial du coteneur.
    COPY CRUD_Country.py . 
    # Cette commande signifie que le conteneur va utiliser le port 5000. Ce qui est utile pour les scripts Python qui démarre des serveur, comme #l'API Flask.
    EXPOSE 5000  
    # Cette commande permet de d'exécuter le script Python CRUD_Country.py via la commande python.
    CMD ["python", "CRUD_Country.py"]

Logique du docker-compose.yml:
    Le fichier définit 2 services principaux et leurs configurations :
        - backend : Il est responsable de l'application backend, à savoir le script 'CRUD_Country.py'. Pour de ce qui est des éléments de configuration :
            => build : l'application est construite à partir du répertoire nommé ./backend
            => container_name : qui correspond au nom du conteneur, qui est backend_service
            => depends_on : cet élément s'adapte au service db il sera donc lancé après le service db.
            => environments :  tout ce qui se trouve dans cette zone sont les variables pour se connecter à la base de données MYSQL :
                • MYSQL_HOST : l'hôte de la base de donnée
                • MYSQL_USER : l'identifiant pour accéder à la base
                • MYSQL_PASSWORD : mot de passe pour se connecter à la base de donnée
                • MYSQL_DATABASE : nom de la base de donnée
            => volumes : le répertoire local est monté dans le conteneur dans l'emplacement défini, à savoir ./data:/app/data, ce qui permet donc de partager des fichier entre l'hôte et le conteneur.
            => networks : elle permet la communication avec les autres services.

        - db : Service responsable de la base de donnée MYSQL, voici les éléments de configuration
            => image : Image docker utilisé pour la base de donnée : mysql:8
            => container_name : Nom du conteneur est db_service
            => restart : Grâce au 'restart : always' le service redémarre automatiquement dans le cas où il échoue
            => environment : Variables qui configurent la base de donnée MYSQl :
                • MYSQL_ROOT_PASSWORD : Mot de passe utilisateur
                • MYSQL_USER : utilisateur MYSQL à créer
                • MYSQL_PASSWORD : mot de passe lié à l'utilisateur
                • MYSQL_DATABASE : Nom de la base de donnée qui est créer
            => ports : le port utilisé pour MYSQL est le 3306, ce qui va permettre un accès à la base de donnée en dehors du conteneur
            => volumes : le volume 'db_data' est utilisé pour gérer les données MYSQL à l'emplacement défini dans le conteneur.
            => networks : Service faisant partie du réseau 'my_network'
    Pour la partie Volumes, il n'y a que db_data expliquant plus haut. Cela évite les pertes de données dès lors que le conteneur db sera supprimé ou redémarré.
    Pour le Networks, il assure la communication entre les services backend et db comme hôtes dans les confirgurations de connexion.

Guide de lancement :
docker build -t python
# Commande permettant de construire l'image du conteneur qui se nomme python
docker-compose up -d
# Commande qui lance tous les services définis dans le fichier docker-compose.yml (-d lance les services en mode détaché, c'est-à-dire qu'ils se lancent en arrière-plan).
docker ps
# La commande permet de vérifier les conteneurs qui sont en cours d'exécution.
docker-compose down
# Cette dernière commande permet d'arrêter l'ensemble des conteneurs qui ont été démarés auparavant.

Explication du code :
    Python : Le script principale permet d'appeler plusieurs chose comme :
        - l'affichage des pays qui se trouve dans la table country
        - ajouter de nouveaux pays
        - supprimer un pays seulement en faisant une recherche via le nom du pays
        - Voir quitter le programme principale

    MYSQL WORKBENCH : La table country contient les informations suivantes :
    - id INT AUTO_INCREMENT PRIMARY KEY,
    - Noms des pays => nom VARCHAR(255) UNIQUE NOT NULL
    - Nombre d'habitants du pays => population_totale BIGINT NOT NULL
    - Leurs capitales => capital VARCHAR(255) NOT NULL
    - Nombre d'habitants de la capitale => ville_plus_peuplee VARCHAR(255) NOT NULL
    - Nom de la ville la plus peuplé => population_ville_plus BIGINT NOT NULL
    - Nombre d'habitants de la ville la plus peuplé =>
    - Nom de la ville la moins peuplé => ville_moins_peuplee VARCHAR(255) NOT NULL
    - Nombre d'habitants de la ville la plus moins => population_ville_moins BIGINT NOT NULL

    En résumé, voici les grandes lignes de la logique métier :
     - Connexion à la base de données MySQL pour interagir avec les données des pays.
     - Opérations CRUD (création, lecture, mise à jour, suppression) sur les informations des pays.
     - Validation et gestion des erreurs pour garantir l'intégrité des données et traiter les erreurs.
     - Exposition via une API ou une interface backend pour permettre l'accès aux données.
    
Optimisation :

    Enfin, nous pouvons optimiser le fichier grâce à quelques solutions importantes comme un "build multi-stage", ce qui permet de séparer les étapes de construction de l'application. Dans cette approche, les outils et dépendances nécessaires pour la construction (comme `pip`) sont installés dans une première étape, tandis que l'image finale ne contient que les fichiers nécessaires, réduisant ainsi la taille de l'image. Une autre optimisation consiste à utiliser des "images de base plus petites", telles que `python:3.11.9-alpine`, qui est beaucoup plus légère que les versions slim, ce qui permet de réduire davantage la taille de l'image. Cependant, il faut s'assurer que toutes les dépendances fonctionnent bien avec cette version minimale, car certaines peuvent nécessiter des bibliothèques système supplémentaires.

    En outre, il est essentiel de "réduire le nombre de couches" en regroupant les commandes `RUN`, `COPY`, et autres dans une seule instruction. Cela diminue le nombre de métadonnées créées et optimise la taille de l'image. Une autre optimisation concerne l'"utilisation du cache Docker". En plaçant les commandes `COPY requirements.txt` avant d’ajouter d’autres fichiers, Docker peut mieux gérer le cache et éviter de réinstaller les dépendances à chaque modification du code, ce qui accélère la construction des images. Ces optimisations combinées permettent non seulement de réduire la taille de l'image, mais aussi d'améliorer les temps de construction et de déploiement.