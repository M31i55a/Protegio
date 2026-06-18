import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("\n" + "=" * 70)
print("TEST AVEC AUTHENTIFICATION")
print("=" * 70 + "\n")

# Créer un utilisateur de test
try:
    user = User.objects.get(username='testuser')
except User.DoesNotExist:
    user = User.objects.create_user(username='testuser', password='testpass')
    print("✓ Utilisateur de test créé\n")

client = Client()

# Se connecter
login_success = client.login(username='testuser', password='testpass')
print(f"Connexion: {'✓ OK' if login_success else '✗ Échouée'}\n")

# Accéder au dashboard
response = client.get('/dashboard/')
print(f"Status code: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode()
    
    keywords = [
        'EXPLOITATION',
        'DIG-MX Tool',
        'SQLMap Scanner',
        'Nikto Scanner',
        'burp_suite Suite',
    ]
    
    print("\nMots clés trouvés:")
    for keyword in keywords:
        count = content.count(keyword)
        status = "✓" if count > 0 else "✗"
        print(f"{status} '{keyword}': {count} fois" if count > 0 else f"{status} '{keyword}': NOT TROUVÉ")
    
    # Vérifier les URLs
    print("\nURLs des outils:")
    for url in ['/dig-mx/', '/sqlmap/', '/nikto/', '/burp-suite/']:
        count = content.count(url)
        print(f"{'✓' if count > 0 else '✗'} {url}: {count} fois" if count > 0 else f"✗ {url}: NOT TROUVÉ")
        
else:
    print(f"✗ Erreur: {response.status_code}")
    if 'Location' in response:
        print(f"Redirection vers: {response['Location']}")

print("\n" + "=" * 70 + "\n")
