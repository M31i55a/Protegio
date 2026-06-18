import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client

client = Client()

print("\n" + "=" * 80)
print("VÉRIFICATION DES URLs CORRIGÉES".center(80))
print("=" * 80 + "\n")

endpoints = [
    ('/dig-mx/', 'DIG MX Tool'),
    ('/burp-suite/', 'burp_suite Suite'),
    ('/sqlmap/', 'SQLMap Scanner'),
    ('/nikto/', 'Nikto Scanner'),
    ('/dashboard/', 'Dashboard'),
]

print("Test des endpoints:\n")
all_ok = True

for endpoint, name in endpoints:
    response = client.get(endpoint, follow=True)
    status = response.status_code
    ok = status == 200
    all_ok = all_ok and ok
    symbol = "✓" if ok else "✗"
    print(f"{symbol} {name:25} ({endpoint:20}): HTTP {status}")

print("\n" + "=" * 80)
if all_ok:
    print("✓ TOUS LES ENDPOINTS SONT MAINTENANT ACCESSIBLES!".center(80))
else:
    print("⚠ CERTAINS ENDPOINTS RETOURNENT DES ERREURS".center(80))
print("=" * 80 + "\n")
