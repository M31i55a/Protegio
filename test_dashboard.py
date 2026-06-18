import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

# Créer ou récupérer un utilisateur admin
admin, created = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})
if created:
    admin.set_password('admin')
    admin.save()

c = Client()
c.force_login(admin)

r = c.get('/dashboard/')

print("\n" + "=" * 60)
print("VÉRIFICATION DU DASHBOARD".center(60))
print("=" * 60)
print(f'\nStatus Code: {r.status_code}')

checks = [
    ('EXPLOITATION', 'Section Exploitation'),
    ('DIG-MX', 'DIG-MX Tool'),
    ('burp_suite Suite', 'burp_suite Suite'),
    ('Nikto', 'Nikto Scanner'),
    ('SQLMap', 'SQLMap Scanner'),
]

content = r.content.decode()
for text, label in checks:
    if text in content:
        print(f'✓ {label}')
    else:
        print(f'✗ {label} - NON TROUVÉ')

print("\n" + "=" * 60 + "\n")
