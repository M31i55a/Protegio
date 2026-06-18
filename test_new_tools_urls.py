import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.urls import get_resolver

resolver = get_resolver()

print("=" * 60)
print("VÉRIFICATION DES URLs DES NOUVEAUX OUTILS")
print("=" * 60)

outils = ['dig-mx', 'sqlmap', 'nikto', 'burp_suite']
found_outils = []

for pattern in resolver.url_patterns:
    pattern_str = str(pattern.pattern)
    for outil in outils:
        if outil in pattern_str:
            found_outils.append(f"✓ {outil}: {pattern_str}")
            print(f"✓ {outil}: {pattern_str}")

if len(found_outils) == len(outils):
    print("\n✓ Toutes les URLs sont correctement enregistrées!")
else:
    print(f"\n✗ Attention: Seulement {len(found_outils)}/{len(outils)} outils trouvés")

print("=" * 60)
