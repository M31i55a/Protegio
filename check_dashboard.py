import os
import django
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

print("\n" + "=" * 60)
print("DEBUG DASHBOARD".center(60))
print("=" * 60 + "\n")

if 'tools-category exploitation' in content:
    print('✓ Classe exploitation trouvée')
if 'Phase offensive' in content:
    print('✓ Sous-titre Phase offensive trouvé')
if 'EXPLOITATION' in content:
    print('✓ Texte EXPLOITATION trouvé')

print("\n" + "=" * 60 + "\n")
