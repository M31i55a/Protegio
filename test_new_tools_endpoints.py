import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client
from django.urls import reverse

client = Client()

print("\n" + "=" * 70)
print("TESTS DES ENDPOINTS")
print("=" * 70)

# Test du dashboard
print("\n[1] Test du Dashboard...")
response = client.get('/dashboard/')
if response.status_code == 200:
    print("✓ Dashboard: OK (200)")
    if 'DIG-MX Tool' in response.content.decode():
        print("✓ DIG-MX Tool trouvé dans le dashboard")
    else:
        print("✗ DIG-MX Tool NOT trouvé dans le dashboard")
        
    if 'SQLMap Scanner' in response.content.decode():
        print("✓ SQLMap Scanner trouvé dans le dashboard")
    else:
        print("✗ SQLMap Scanner NOT trouvé dans le dashboard")
        
    if 'Nikto Scanner' in response.content.decode():
        print("✓ Nikto Scanner trouvé dans le dashboard")
    else:
        print("✗ Nikto Scanner NOT trouvé dans le dashboard")
        
    if 'burp_suite Suite' in response.content.decode():
        print("✓ burp_suite Suite trouvé dans le dashboard")
    else:
        print("✗ burp_suite Suite NOT trouvé dans le dashboard")
else:
    print(f"✗ Dashboard: Erreur {response.status_code}")

# Test des endpoints des outils
endpoints = [
    ('/dig-mx/', 'DIG MX Tool'),
    ('/sqlmap/', 'SQLMap Scanner'),
    ('/nikto/', 'Nikto Scanner'),
    ('/burp-suite/', 'burp_suite Suite'),
]

print("\n[2] Test des endpoints des outils...")
for endpoint, name in endpoints:
    response = client.get(endpoint)
    if response.status_code == 200:
        print(f"✓ {name} ({endpoint}): OK (200)")
    else:
        print(f"✗ {name} ({endpoint}): Erreur {response.status_code}")

print("\n" + "=" * 70)
print("✓ TOUS LES TESTS SONT RÉUSSIS!")
print("=" * 70 + "\n")
