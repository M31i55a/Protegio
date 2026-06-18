import os, django
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

# Trouver les positions des outils
tools = ['DIG-MX Tool', 'SQLMap Scanner', 'Nikto Scanner', 'burp_suite Suite']
positions = []
for tool in tools:
    pos = content.find(tool)
    positions.append((tool, pos))
    print(f"{tool}: position {pos}")

# Trouver la position de EXPLOITATION
exp_pos = content.find('EXPLOITATION')
print(f"\nEXPLOITATION: position {exp_pos}")

# Vérifier la fin du contenu
print(f"\nDerniers 200 caractères:")
print(content[-200:])
