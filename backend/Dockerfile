FROM python:3.11.9-slim  
# Définition du répertoire de travail
WORKDIR /app
# Copie des fichiers nécessaires
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  
# Copie du script Python
COPY CRUD_Country.py . 
# Exposition du port (si une API Flask par exemple)
EXPOSE 5000  
# Commande de démarrage
CMD ["python", "CRUD_Country.py"]