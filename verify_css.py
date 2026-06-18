#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client

client = Client()

print("\n" + "=" * 70)
print("VERIFICATION DES AMELIORATIONS CSS")
print("=" * 70)

# Test all pages and check for new CSS classes
pages = [
    ('/integrations/nuclei/', 'Nuclei Scanner'),
    ('/integrations/ports/', 'Port Scanner'),
    ('/integrations/ssl/', 'SSL/TLS Checker'),
    ('/integrations/api-security/', 'API Security'),
    ('/integrations/cve/', 'CVE Lookup'),
]

print("\nVérification des classes CSS...")
print("-" * 70)

all_good = True
for url, name in pages:
    response = client.get(url)
    content = response.content.decode()
    
    # Check if new CSS classes are present
    css_features = {
        'Tables': '<table' in content,
        'Badges': 'badge' in content,
        'Cards': 'card' in content,
        'Responsive': '<div class="container' in content or '<div class="row' in content,
    }
    
    status = '✓' if all(css_features.values()) else '✗'
    all_good = all_good and all(css_features.values())
    print(f"{name:<25} {status}")

print("-" * 70)
if all_good:
    print("✓ Tous les éléments CSS sont appliqués correctement!")
else:
    print("⚠ Certains éléments CSS pourraient manquer")

print("=" * 70 + "\n")
