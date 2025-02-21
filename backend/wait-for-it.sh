#!/bin/sh

# Afficher les valeurs des variables
echo "MYSQL_HOST: $MYSQL_HOST"
echo "MYSQL_PORT: $MYSQL_PORT"

# Attendre que MySQL soit prêt
echo "⏳ En attente que MySQL soit prêt sur $MYSQL_HOST:$MYSQL_PORT..."

while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  sleep 1
done

echo "✅ MySQL est prêt ! Lancement de l'application..."

# Lancer l'application Flask
exec python CRUD_Country.py  # Exécute directement votre application