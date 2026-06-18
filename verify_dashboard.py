import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model
User = get_user_model()
admin, _ = User.objects.get_or_create(username='admin')
c = Client()
c.force_login(admin)
r = c.get('/dashboard/')
content = r.content.decode()

print("\n✓ Réponse reçue, status:", r.status_code)
print("✓ Taille du contenu:", len(content))

# Chercher les 4 outils
tools = ['DIG-MX Tool', 'SQLMap Scanner', 'Nikto Scanner', 'burp_suite Suite']
for tool in tools:
    if tool in content:
        print(f"✓ {tool} trouvé")
    else:
        print(f"✗ {tool} NON trouvé")

# Chercher Exploitation
if 'EXPLOITATION' in content:
    print("✓ Section EXPLOITATION trouvée")
elif 'Phase offensive' in content:
    print("✓ Sous-titre 'Phase offensive' trouvé")
else:
    print("✗ Aucun signe de la section Exploitation")

# Chercher tools-category exploitation
if 'tools-category exploitation' in content:
    print("✓ Classe CSS 'tools-category exploitation' trouvée")
else:
    print("✗ Classe CSS 'tools-category exploitation' NOT trouvée")

print("\nDébut du contenu:")
print(content[:300])
