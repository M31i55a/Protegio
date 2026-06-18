# 🚀 Guide de Déploiement sur VPS Contabo

## Prérequis
- Putty ou autre client SSH
- Serveur VPS Contabo: `173.249.53.53`
- Identifiants root

---

## 📋 Étapes de Déploiement Détaillées

### Étape 0: Connexion SSH avec Putty

1. Ouvrez **Putty**
2. Entrez l'IP: `173.249.53.53`
3. Port: `22`
4. Cliquez sur "Open"
5. Login: `root`
6. Password: [votre mot de passe root]

---

### ✅ Option 1: Déploiement Automatique (RECOMMANDÉ)

Une fois connecté au serveur, exécutez:

```bash
cd /root && curl -fsSL https://raw.githubusercontent.com/brivelharold17-cyber/Protegio_Tool/master/deploy.sh | bash
```

Ou si vous préférez le fichier local:

```bash
cd /root/Protegio_Tool
bash deploy.sh
```

**Attendez que le script se termine (5-10 minutes)**

---

### ✅ Option 2: Déploiement Manuel Étape par Étape

**Copier-coller chaque bloc une par une dans Putty**

#### Étape 1: Mise à jour du système
```bash
apt update
apt upgrade -y
```

#### Étape 2: Installation de Docker
```bash
apt install -y docker.io docker-compose git curl
systemctl start docker
systemctl enable docker
```

#### Étape 3: Clonage du code
```bash
cd /root
git clone https://github.com/brivelharold17-cyber/Protegio_Tool.git
cd Protegio_Tool
```

#### Étape 4: Démarrage des conteneurs
```bash
docker compose up -d
```

*Attendez 30 secondes...*

#### Étape 5: Migrations base de données
```bash
docker compose exec -T web python manage.py migrate --noinput
```

#### Étape 6: Fichiers statiques
```bash
docker compose exec -T web python manage.py collectstatic --noinput
```

#### Étape 7: Création du compte admin
```bash
docker compose exec -T web python manage.py shell -c \
  "from django.contrib.auth import get_user_model; \
   User = get_user_model(); \
   User.objects.filter(username='admin').delete(); \
   u = User.objects.create_superuser('admin', 'admin@example.local', 'admin123456'); \
   print(f'✅ Admin créé: {u.username}')"
```

#### Étape 8: Vérification
```bash
docker compose ps
```

**Vous devriez voir 3 conteneurs "Up":**
- unified_tool-db-1 (PostgreSQL)
- unified_tool-web-1 (Django/Gunicorn)
- unified_tool-caddy-1 (Reverse Proxy)

---

## 🌐 Accès à l'Application

Une fois le déploiement terminé:

| Service | URL |
|---------|-----|
| **Application** | http://173.249.53.53 |
| **Admin Django** | http://173.249.53.53/admin/ |
| **HTTPS (TLS)** | https://173.249.53.53 |

**Identifiants Admin:**
- Username: `admin`
- Password: `admin123456`

---

## 🔍 Commandes de Gestion Utiles

```bash
# Voir l'état des conteneurs
docker compose ps

# Voir les logs en temps réel
docker compose logs -f

# Voir les logs d'une service particulière
docker compose logs web
docker compose logs caddy
docker compose logs db

# Redémarrer les services
docker compose restart

# Arrêter les services
docker compose down

# Redémarrer avec reconstruction
docker compose down -v
docker compose up -d

# Accès shell Django
docker compose exec web python manage.py shell

# Créer un nouvel admin
docker compose exec -T web python manage.py createsuperuser

# Vider le cache
docker compose exec -T web python manage.py clear_cache
```

---

## ⚠️ Troubleshooting

### Caddy ne démarre pas
```bash
docker compose logs caddy
docker compose restart caddy
```

### Port 80/443 déjà utilisé
```bash
# Vérifier quel processus utilise le port
lsof -i :80
lsof -i :443

# Ou arrêter les anciens conteneurs
docker compose down -v
docker system prune -af
docker compose up -d
```

### Problème de connexion à la BDD
```bash
docker compose exec -T web python manage.py dbshell
docker compose logs db
```

### Réinitialiser complètement
```bash
cd /root/Protegio_Tool
docker compose down -v
rm -rf postgres_data/
git pull origin master
docker compose up -d
docker compose exec -T web python manage.py migrate --noinput
docker compose exec -T web python manage.py collectstatic --noinput
```

---

## 📝 Notes

- Les données de la base de données sont persistantes dans `postgres_data/`
- Les fichiers statiques sont dans `staticfiles/`
- Les logs sono accessibles en temps réel avec `docker compose logs -f`
- Le certificat SSL peut prendre quelques minutes à se générer (Caddy utilise Let's Encrypt)

---

## ✅ Vérification Finale

```bash
# Vérifier que l'app répond
curl -I http://173.249.53.53

# Résultat attendu:
# HTTP/1.1 200 OK
```

---

**C'est fait! 🎉 Votre Protegio Tool est en ligne!**
