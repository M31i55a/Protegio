# Configuration d'authentification OAuth - PROTEGIO

## Vue d'ensemble
Le système d'authentification PROTEGIO supporte maintenant les fournisseurs OAuth suivants:
- **Google**
- **Microsoft**
- **GitHub**

## 1. Installation des dépendances

Les packages requis ont été ajoutés à `requirements.txt`:
```bash
pip install -r requirements.txt
```

## 2. Migrations Django

Exécutez les migrations pour configurer les tables nécessaires:
```bash
python manage.py migrate
```

## 3. Créer un site Django

1. Allez sur l'admin Django: `http://localhost:8000/admin/`
2. Accédez à **Sites** > **Add Site**
3. Remplissez:
   - **Domain name**: `localhost:8000` (pour développement) ou votre domaine
   - **Name**: `PROTEGIO`
4. Cliquez sur **Save**

## 4. Configuration Google OAuth

### Étape 1: Créer un projet Google Cloud

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un existant
3. Activez l'API Google+ (deprecated) ou utilisez Google Identity
4. Allez sur **Credentials**
5. Créez un **OAuth 2.0 Client ID**:
   - Type: **Web application**
   - Authorized redirect URIs:
     ```
     http://localhost:8000/accounts/google/login/callback/
     https://votre-domaine.com/accounts/google/login/callback/
     ```

### Étape 2: Ajouter à Django

1. Admin Django: `http://localhost:8000/admin/`
2. Accédez à **Social applications** > **Add Social application**
3. Remplissez:
   - **Provider**: Google
   - **Name**: Google
   - **Client id**: (depuis Google Cloud Console)
   - **Secret key**: (depuis Google Cloud Console)
   - **Sites**: Sélectionnez votre site
4. Cliquez sur **Save**

## 5. Configuration Microsoft OAuth

### Étape 1: Créer une application Azure

1. Allez sur [Azure Portal](https://portal.azure.com/)
2. Allez sur **Azure Active Directory** > **App registrations**
3. Créez une **New registration**:
   - **Name**: PROTEGIO
   - **Supported account types**: Multitenant
   - **Redirect URI**: Web
     ```
     http://localhost:8000/accounts/microsoft/login/callback/
     https://votre-domaine.com/accounts/microsoft/login/callback/
     ```

### Étape 2: Générer les secrets

1. Allez sur **Certificates & secrets**
2. Créez un **New client secret**
3. Copiez la valeur du secret
4. Allez sur **API permissions** et accordez les permissions nécessaires

### Étape 3: Ajouter à Django

1. Admin Django
2. **Social applications** > **Add Social application**
3. Remplissez:
   - **Provider**: Microsoft
   - **Name**: Microsoft
   - **Client id**: (Application ID depuis Azure)
   - **Secret key**: (Client secret)
   - **Sites**: Sélectionnez votre site
4. Cliquez sur **Save**

## 6. Configuration GitHub OAuth

### Étape 1: Créer une OAuth App

1. Allez sur [GitHub Settings > Developer settings > OAuth Apps](https://github.com/settings/developers)
2. Créez une **New OAuth App**:
   - **Application name**: PROTEGIO
   - **Homepage URL**: `http://localhost:8000` ou votre URL
   - **Authorization callback URL**:
     ```
     http://localhost:8000/accounts/github/login/callback/
     https://votre-domaine.com/accounts/github/login/callback/
     ```

### Étape 2: Ajouter à Django

1. Admin Django
2. **Social applications** > **Add Social application**
3. Remplissez:
   - **Provider**: GitHub
   - **Name**: GitHub
   - **Client id**: (Client ID depuis GitHub)
   - **Secret key**: (Client Secret)
   - **Sites**: Sélectionnez votre site
4. Cliquez sur **Save**

## 7. Personnalisations du dashboard

Après l'authentification réussie, les utilisateurs sont automatiquement redirigés vers le dashboard des outils.

### Flux d'authentification:

1. **Page de login/signup** - Utilisateur choisit un fournisseur
2. **Redirection OAuth** - Redirection vers le fournisseur
3. **Authentification** - L'utilisateur se connecte chez le fournisseur
4. **Callback** - Redirection vers `LOGIN_REDIRECT_URL`
5. **Dashboard** - Accès au tableau de bord des outils

### Modèle utilisateur étendu

Pour ajouter des informations personnalisées après une connexion OAuth:

```python
# apps/accounts/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=[
        ('google', 'Google'),
        ('microsoft', 'Microsoft'),
        ('github', 'GitHub'),
        ('manual', 'Manual Email/Password')
    ])
    avatar = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.account_type}"
```

## 8. Vérification

### Test en local:

1. Démarrez le serveur:
   ```bash
   python manage.py runserver
   ```

2. Allez sur `http://localhost:8000/accounts/signup/`

3. Vous devriez voir les boutons OAuth (Google, Microsoft, GitHub)

4. Cliquez sur l'un d'eux et testez le flux d'authentification

## 9. Dépannage

### Erreur: "No such table: socialaccount_socialapp"
```bash
python manage.py migrate
```

### Erreur: "Site matching query does not exist"
- Assurez-vous d'avoir créé le site dans la section **Sites** de l'admin

### OAuth callback ne fonctionne pas
- Vérifiez l'URI de callback dans la console du fournisseur
- Assurez-vous que le domaine correspond exactement

### Les données utilisateur ne se synchronisent pas
- Vérifiez les logs Django pour les erreurs
- Vérifiez que les scopes OAuth sont correctement configurés

## 10. Configuration en production

Pour la production, mettez à jour:

1. **settings.py**:
   ```python
   ALLOWED_HOSTS = ['votre-domaine.com']
   DEBUG = False
   CSRF_TRUSTED_ORIGINS = ['https://votre-domaine.com']
   ```

2. **Créez un nouveau site** dans l'admin Django avec votre domaine de production

3. **Mettez à jour les URIs de callback** dans chaque console OAuth (Google, Microsoft, GitHub)

4. **Utilisez HTTPS** en production
