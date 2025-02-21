# Utilisation de l'image officielle Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer le client MySQL et netcat
RUN apt-get update && \
    apt-get install -y default-mysql-client netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copier les fichiers nécessaires
COPY requirements.txt .

# Mettre à jour pip puis installer les dépendances
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier wait-for-it.sh et donner les permissions d'exécution
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copier le reste de l'application
COPY . .

# Donner les permissions d'accès au dossier templates
RUN chmod -R 755 /app/templates

# Exposer le port Flask
EXPOSE 5000

# Utilisation de wait-for-it pour attendre que MySQL soit prêt
CMD ["/wait-for-it.sh"]
