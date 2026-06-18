#!/bin/bash

# Script de déploiement automatique pour Contabo VPS
# Exécutez avec: bash deploy.sh

set -e

echo "======================================"
echo "Déploiement Protegio Tool sur VPS"
echo "======================================"

# Étape 1: Mise à jour du système
echo ""
echo "[ÉTAPE 1/6] Mise à jour du système..."
apt update
apt upgrade -y

# Étape 2: Installation de Docker et Docker Compose
echo ""
echo "[ÉTAPE 2/6] Installation de Docker et Docker Compose..."
apt install -y docker.io docker-compose git curl
systemctl start docker
systemctl enable docker

# Étape 3: Clonage du repository
echo ""
echo "[ÉTAPE 3/6] Clonage du repository GitHub..."
cd /root
if [ -d "Protegio_Tool" ]; then
    rm -rf Protegio_Tool
fi
git clone https://github.com/brivelharold17-cyber/Protegio_Tool.git
cd Protegio_Tool

# Étape 4: Démarrage des services Docker
echo ""
echo "[ÉTAPE 4/6] Démarrage des services Docker..."
docker compose up -d

# Attendre que les services soient prêts
sleep 10

# Étape 5: Migrations de base de données
echo ""
echo "[ÉTAPE 5/6] Exécution des migrations..."
docker compose exec -T web python manage.py migrate --noinput

# Étape 6: Collecte des fichiers statiques
echo ""
echo "[ÉTAPE 6/6] Collecte des fichiers statiques..."
docker compose exec -T web python manage.py collectstatic --noinput

# Création du superuser
echo ""
echo "Création du compte administrateur..."
docker compose exec -T web python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').delete(); u = User.objects.create_superuser('admin', 'admin@example.local', 'admin123456'); print(f'Admin créé: {u.username}')"

# Vérification
echo ""
echo "======================================"
echo "Vérification du déploiement..."
echo "======================================"
docker compose ps

echo ""
echo "✅ Déploiement terminé avec succès!"
echo ""
echo "Accédez à votre application:"
echo "  • HTTP:  http://173.249.53.53"
echo "  • HTTPS: https://173.249.53.53"
echo "  • Admin: http://173.249.53.53/admin/"
echo ""
echo "Identifiants admin:"
echo "  • Username: admin"
echo "  • Password: admin123456"
echo ""
echo "Commandes utiles:"
echo "  • Voir les logs: docker compose logs"
echo "  • Redémarrer: docker compose restart"
echo "  • Arrêter: docker compose down"
echo "======================================"
