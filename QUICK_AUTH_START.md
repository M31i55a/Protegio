# Guide de démarrage - Authentification OAuth PROTEGIO

## Installation et configuration initiale

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Exécuter les migrations

```bash
# Migrations Django principales
python manage.py migrate

# Créer le superuser (admin)
python manage.py createsuperuser
```

### 3. Configuration initiale du site et OAuth

```bash
# Exécuter le script de configuration
python setup_oauth.py
```

### 4. Démarrer le serveur de développement

```bash
python manage.py runserver
```

Accédez à: `http://localhost:8000`

---

## Configuration des fournisseurs OAuth

### Accéder à l'admin Django

1. Allez sur: `http://localhost:8000/admin/`
2. Connectez-vous avec votre compte superuser

### Configurer Google OAuth

**Voir `OAUTH_SETUP.md` - Section "Configuration Google OAuth"**

Après avoir créé votre projet Google:
1. Admin Django → Social applications → Add Social application
2. Provider: **Google**
3. Name: **Google**
4. Client id: (votre Google Client ID)
5. Secret key: (votre Google Client Secret)
6. Sites: Sélectionnez votre site

### Configurer Microsoft OAuth

**Voir `OAUTH_SETUP.md` - Section "Configuration Microsoft OAuth"**

Après avoir créé votre application Azure:
1. Admin Django → Social applications → Add Social application
2. Provider: **Microsoft**
3. Name: **Microsoft**
4. Client id: (votre Azure Application ID)
5. Secret key: (votre Azure Client Secret)
6. Sites: Sélectionnez votre site

### Configurer GitHub OAuth

**Voir `OAUTH_SETUP.md` - Section "Configuration GitHub OAuth"**

Après avoir créé votre OAuth App GitHub:
1. Admin Django → Social applications → Add Social application
2. Provider: **GitHub**
3. Name: **GitHub**
4. Client id: (votre GitHub Client ID)
5. Secret key: (votre GitHub Client Secret)
6. Sites: Sélectionnez votre site

---

## Tester l'authentification

### Inscription avec OAuth

1. Allez sur: `http://localhost:8000/accounts/signup/`
2. Cliquez sur l'un des fournisseurs (Google, Microsoft, GitHub)
3. Autorisez l'application auprès du fournisseur
4. Vous serez redirigé et connecté au dashboard

### Connexion avec OAuth

1. Allez sur: `http://localhost:8000/accounts/login/`
2. Cliquez sur votre fournisseur préféré
3. Vous serez redirigé vers le dashboard

### Inscription manuelle

1. Allez sur: `http://localhost:8000/accounts/signup/`
2. Cliquez sur "Manual Signup"
3. Remplissez le formulaire (username, email, password)
4. Cliquez sur "Create Account"

---

## Structure des pages d'authentification

### Login Page: `/accounts/login/`
- Social OAuth buttons (Google, Microsoft, GitHub)
- Manual email/password login form
- Link to signup page

### Signup Page: `/accounts/signup/`
- Two tabs:
  - **Social Login**: Quick signup avec OAuth providers
  - **Manual Signup**: Traditional email/password signup

### Profile Page: `/accounts/profile/` (après connexion)
- Affiche les informations du compte
- Liste les comptes sociaux connectés
- Option pour connecter/déconnecter des comptes sociaux

---

## Après la connexion

### Dashboard PROTEGIO

1. Après l'authentification réussie, l'utilisateur est redirigé vers: `/dashboard/`

2. Le dashboard affiche:
   - Les informations du profil utilisateur
   - Les comptes sociaux connectés
   - Les outils de sécurité disponibles

3. Les utilisateurs peuvent:
   - Accéder à tous les outils PROTEGIO
   - Gérer leur profil
   - Connecter/déconnecter des comptes sociaux

---

## Dépannage

### Erreur: "Site matching query does not exist"

```bash
# Vérifiez que le site est configuré
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> Site.objects.all()
```

Si vide:
```python
>>> Site.objects.create(id=1, name='PROTEGIO', domain='localhost:8000')
```

### Erreur: "No such table: socialaccount_socialapp"

Exécutez les migrations:
```bash
python manage.py migrate
```

### OAuth callback échoue

1. Vérifiez le fichier URI de callback dans votre console OAuth
2. Assurez-vous que l'URI corresponds exactement à:
   `http://localhost:8000/accounts/{provider}/login/callback/`
3. Vérifiez que la Social application est configurée dans l'admin Django

### L'utilisateur n'est pas redirigé vers le dashboard

Vérifiez dans settings.py:
```python
LOGIN_REDIRECT_URL = 'dashboard:dashboard'
```

---

## Configuration en production

Pour déployer en production:

1. **Mettez à jour `settings.py`:**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['votre-domaine.com', 'www.votre-domaine.com']
   ```

2. **Créez un nouveau site dans l'admin** avec votre domaine de production

3. **Mettez à jour les URIs OAuth** chez chaque fournisseur:
   - Google: `https://votre-domaine.com/accounts/google/login/callback/`
   - Microsoft: `https://votre-domaine.com/accounts/microsoft/login/callback/`
   - GitHub: `https://votre-domaine.com/accounts/github/login/callback/`

4. **Utilisez HTTPS** en production

5. **Secrets de sécurité:**
   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

---

## Architecture de sécurité

- Toutes les authentifications utilisent OAuth 2.0
- Les mots de passe ne sont pas stockés pour les comptes sociaux
- Les tokens OAuth sont gérés par django-allauth
- Les comptes sociaux sont liés à un utilisateur Django unique

---

## Support et documentation

- Documentation django-allauth: https://django-allauth.readthedocs.io/
- OAuth 2.0 Specification: https://tools.ietf.org/html/rfc6749
- Fichier complet: `OAUTH_SETUP.md`
