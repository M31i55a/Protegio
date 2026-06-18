import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()
from django.test import Client

c = Client()

print("\n" + "=" * 80)
print("VÉRIFICATION DES TEMPLATES COPIÉS".center(80))
print("=" * 80 + "\n")

endpoints = [
    ('/burp-suite/', 'burp_suite Suite'),
    ('/dig-mx/', 'DIG MX Tool'),
    ('/nikto/', 'Nikto Scanner'),
    ('/sqlmap/', 'SQLMap Scanner'),
]

for endpoint, name in endpoints:
    try:
        r = c.get(endpoint)
        if r.status_code == 200:
            print(f"✓ {name:25} ({endpoint:20}): HTTP {r.status_code} - OK")
        else:
            print(f"✗ {name:25} ({endpoint:20}): HTTP {r.status_code}")
    except Exception as e:
        print(f"✗ {name:25} ({endpoint:20}): ERREUR - {str(e)[:50]}")

print("\n" + "=" * 80)
print("Tests terminés!".center(80))
print("=" * 80 + "\n")
