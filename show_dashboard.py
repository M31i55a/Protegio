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
# Chercher Exploitation
idx = content.find('EXPLOITATION')
if idx > 0:
    print(content[max(0, idx-100):min(len(content), idx+200)])
else:
    print("EXPLOITATION not found")
    # Chercher tools-category
    idx = content.find('tools-category')
    if idx > 0:
        print("\nFound 'tools-category' at position", idx)
        print(content[max(0, idx-50):min(len(content), idx+300)])
    else:
        print("tools-category not found either")
