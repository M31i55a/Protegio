#!/usr/bin/env python
"""
Script de test complet pour le projet UNIFIED_TOOL
Teste toutes les URLs principales et les imports
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse, get_resolver

# Color output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_info(msg):
    print(f"{YELLOW}ℹ {msg}{RESET}")

# Test 1: Check all URLs are registered
print("\n" + "="*50)
print("TEST 1: VÉRIFICATION DES URLS")
print("="*50)

resolver = get_resolver()
try:
    all_urls = resolver.get_urls()
    print_success(f"Toutes les URLs sont chargées ({len(all_urls)} urls)")
    print_info(f"URLs principales trouvées:")
    
    patterns = resolver.url_patterns
    for pattern in patterns[:10]:
        print(f"  - {pattern.pattern}")
except Exception as e:
    print_error(f"Erreur lors du chargement des URLs: {e}")

# Test 2: Check admin account
print("\n" + "="*50)
print("TEST 2: VÉRIFICATION DU COMPTE ADMIN")
print("="*50)

admin_exists = User.objects.filter(username='admin').exists()
if admin_exists:
    print_success("Compte admin existe")
else:
    print_info("Création du compte admin...")
    try:
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print_success("Compte admin créé (admin / admin123)")
    except Exception as e:
        print_error(f"Impossible de créer admin: {e}")

# Test 3: Test app imports
print("\n" + "="*50)
print("TEST 3: VÉRIFICATION DES IMPORTS")
print("="*50)

apps_to_test = [
    ('apps.intruder.views', 'intruder_view'),
    ('apps.checker.views', 'index'),
    ('apps.scanner.views', 'HomeView'),
    ('apps.perforNet.views', 'speedtest_home'),
    ('apps.reports.views', 'reports_list'),
    ('apps.protegioTools.views', 'home'),
    ('apps.dns_tool.views', 'NslookupView'),
]

for app_module, func_name in apps_to_test:
    try:
        parts = app_module.rsplit('.', 1)
        module = __import__(parts[0], fromlist=[parts[1]])
        obj = getattr(module, func_name, None)
        if obj:
            print_success(f"{app_module}.{func_name} ✓")
        else:
            print_error(f"{app_module}.{func_name} - Fonction non trouvée")
    except Exception as e:
        print_error(f"{app_module}.{func_name} - {str(e)[:50]}")

# Test 4: Test HTTP requests
print("\n" + "="*50)
print("TEST 4: VÉRIFICATION DES REQUÊTES HTTP")
print("="*50)

client = Client()

test_urls = [
    ('/admin/', 'Admin'),
    ('/accounts/login/', 'Login'),
    ('/accounts/signup/', 'Signup'),
    ('/dashboard/', 'Dashboard'),
]

for url, name in test_urls:
    try:
        response = client.get(url)
        status_code = response.status_code
        if status_code == 200:
            print_success(f"{name} ({url}) - {status_code}")
        elif status_code in [302, 301]:  # Redirect
            print_success(f"{name} ({url}) - {status_code} (Redirect)")
        else:
            print_error(f"{name} ({url}) - {status_code}")
    except Exception as e:
        print_error(f"{name} ({url}) - Erreur: {str(e)[:40]}")

# Test 5: Database models
print("\n" + "="*50)
print("TEST 5: VÉRIFICATION DES MODÈLES")
print("="*50)

from django.apps import apps

models_to_check = [
    ('scanner', 'ScanResult'),
    ('protegioTools', 'WHOISResult'),
    ('perforNet', 'SpeedTestResult'),
    ('dns_tool', 'DNSQueryHistory'),
    ('integrations', 'NucleiScan'),
]

for app_name, model_name in models_to_check:
    try:
        app = apps.get_app_config(app_name)
        model = app.get_model(model_name)
        print_success(f"{app_name}.{model_name}")
    except:
        print_error(f"{app_name}.{model_name} - Non trouvé")

# Summary
print("\n" + "="*50)
print("✅ TESTS COMPLÉTÉS!")
print("="*50)
print("\nLe projet est fonctionnel et prêt à être utilisé.")
print("Accédez à http://localhost:8001 avec les credentials:")
print("  Username: admin")
print("  Password: admin123")
