#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("\n" + "=" * 80)
print("VÉRIFICATION COMPLÈTE - INTÉGRATION DES 4 NOUVEAUX OUTILS".center(80))
print("=" * 80 + "\n")

# Créer un utilisateur de test
try:
    user = User.objects.get(username='testuser')
except User.DoesNotExist:
    user = User.objects.create_user(username='testuser', password='testpass')

client = Client()
client.login(username='testuser', password='testpass')

# Test 1: URLs enregistrées
print("[1] Vérification des URLs enregistrées...")
print("-" * 80)

from django.urls import get_resolver
resolver = get_resolver()

urls_to_check = [
    ('dig-mx', '/dig-mx/'),
    ('sqlmap', '/sqlmap/'),
    ('nikto', '/nikto/'),
    ('burp_suite', '/burp-suite/'),
]

for name, path in urls_to_check:
    found = False
    for pattern in resolver.url_patterns:
        if name in str(pattern.pattern):
            found = True
            break
    print(f"{'✓' if found else '✗'} URL {path}: {'TROUVÉE' if found else 'MANQUANTE'}")

# Test 2: Dashboard
print("\n[2] Vérification du Dashboard...")
print("-" * 80)

response = client.get('/dashboard/')
if response.status_code == 200:
    content = response.content.decode()
    
    tools = [
        ('DIG-MX Tool', '/dig-mx/'),
        ('SQLMap Scanner', '/sqlmap/'),
        ('Nikto Scanner', '/nikto/'),
        ('burp_suite Suite', '/burp-suite/'),
    ]
    
    all_present = True
    for name, url in tools:
        has_name = name in content
        has_url = url in content
        status = '✓' if (has_name and has_url) else '✗'
        print(f"{status} {name}: nom={has_name}, url={has_url}")
        if not (has_name and has_url):
            all_present = False
    
    if all_present:
        print("\n✓ Tous les outils sont présents dans le dashboard!")
    else:
        print("\n✗ Certains outils sont manquants dans le dashboard")
else:
    print(f"✗ Erreur d'accès au dashboard (status: {response.status_code})")

# Test 3: Endpoints des outils
print("\n[3] Vérification des endpoints des outils...")
print("-" * 80)

endpoints = [
    ('/dig-mx/', 'DIG MX Tool'),
    ('/sqlmap/', 'SQLMap Scanner'),
    ('/nikto/', 'Nikto Scanner'),
    ('/burp-suite/', 'burp_suite Suite'),
]

all_accessible = True
for endpoint, name in endpoints:
    response = client.get(endpoint)
    status = '✓' if response.status_code == 200 else '✗'
    print(f"{status} {name} ({endpoint}): {response.status_code}")
    if response.status_code != 200:
        all_accessible = False

# Test 4: Base de données
print("\n[4] Vérification de la base de données...")
print("-" * 80)

from apps.dig_mx.models import DigMxScan
from apps.sqlmap.models import SqlmapScan
from apps.nikto.models import NiktoScan
from apps.burp_suite_suite.models import burp_suiteScan

models = [
    ('DigMxScan', DigMxScan),
    ('SqlmapScan', SqlmapScan),
    ('NiktoScan', NiktoScan),
    ('burp_suiteScan', burp_suiteScan),
]

for name, model in models:
    try:
        count = model.objects.count()
        print(f"✓ {name}: Table existe ({count} enregistrements)")
    except Exception as e:
        print(f"✗ {name}: Erreur - {str(e)}")

# Résumé final
print("\n" + "=" * 80)
if all_present and all_accessible:
    print("✓ TOUS LES TESTS RÉUSSIS - INTÉGRATION COMPLÈTE!".center(80))
else:
    print("⚠ CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFICATION RECOMMANDÉE".center(80))
print("=" * 80 + "\n")
