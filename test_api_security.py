#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client

client = Client()
response = client.get('/integrations/api-security/')
print(f'HTTP Status: {response.status_code}')
if response.status_code == 200:
    print('✓ Page API Security loaded successfully!')
    if 'api_test_detail' in response.content.decode():
        print('✓ URL correctly mapped in template!')
    else:
        print('⚠ URL might not be correctly displayed')
else:
    print(f'✗ Error: {response.status_code}')
    print(response.content.decode()[:500])
