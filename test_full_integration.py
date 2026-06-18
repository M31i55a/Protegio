import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client

client = Client()

print("\n" + "=" * 70)
print("TEST COMPLET DU DASHBOARD AVEC LES NOUVEAUX OUTILS")
print("=" * 70)

# Test du dashboard avec follow=True
print("\n[1] Accès au Dashboard...")
response = client.get('/dashboard/', follow=True)
if response.status_code == 200:
    print("✓ Dashboard: OK (200)")
else:
    print(f"✗ Dashboard: Erreur {response.status_code}")
    exit(1)

content = response.content.decode()

# Vérifier que tous les outils sont présents
print("\n[2] Vérification de la présence des outils dans la section EXPLOITATION...")

tools = [
    ('DIG-MX Tool', 'dig-mx'),
    ('SQLMap Scanner', 'sqlmap'),
    ('Nikto Scanner', 'nikto'),
    ('burp_suite Suite', 'burp_suite'),
]

all_present = True
for tool_name, tool_id in tools:
    if tool_name in content:
        print(f"✓ {tool_name}: TROUVÉ")
    else:
        print(f"✗ {tool_name}: NOT TROUVÉ")
        all_present = False
    
    # Vérifier aussi les liens
    if f'/burp-suite/' in content or f'/{tool_id}/' in content:
        print(f"  ✓ Lien vers {tool_id} présent")
    else:
        print(f"  ✗ Lien vers {tool_id} manquant")

# Vérifier la section "EXPLOITATION"
if 'EXPLOITATION' in content and 'Phase offensive' in content:
    print("\n✓ Section EXPLOITATION trouvée avec la bonne description")
else:
    print("\n✗ Section EXPLOITATION ou description manquante")
    all_present = False

if all_present:
    print("\n" + "=" * 70)
    print("✓ TOUS LES OUTILS SONT CORRECTEMENT INTÉGRÉS!")
    print("=" * 70)
else:
    print("\n✗ Des outils sont manquants ou mal intégrés")

print("\n[3] Test rapide des pages des outils...")

endpoints = [
    ('/dig-mx/', 'DIG MX Tool'),
    ('/sqlmap/', 'SQLMap Scanner'),
    ('/nikto/', 'Nikto Scanner'),
    ('/burp-suite/', 'burp_suite Suite'),
]

for endpoint, name in endpoints:
    response = client.get(endpoint)
    if response.status_code == 200:
        print(f"✓ {name}: Accessible")
    else:
        print(f"✗ {name}: Erreur {response.status_code}")

print("\n" + "=" * 70 + "\n")
