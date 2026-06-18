import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()
from django.test import Client
c = Client()
print("Testing /burp-suite/")
r1 = c.get('/burp-suite/')
print(f"Status: {r1.status_code}")
print("Testing /dig-mx/")
r2 = c.get('/dig-mx/')
print(f"Status: {r2.status_code}")
print("Done")
