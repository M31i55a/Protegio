#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client
from apps.integrations.models import APISecurityTest

# Get the test we just created
test = APISecurityTest.objects.last()
print(f"Testing API Test Detail page for test ID: {test.id}")

client = Client()
response = client.get(f'/integrations/api-security/{test.id}/')
print(f'HTTP Status: {response.status_code}')

if response.status_code == 200:
    print('✓ API Test Detail page loaded successfully!')
    print(f'✓ Test URL: {test.api_url}')
    print(f'✓ Test Type: {test.get_test_type_display()}')
    print(f'✓ Vulnerable: {test.vulnerable}')
    print(f'✓ Issues Found: {test.issues_found}')
    print(f'✓ Duration: {test.duration}s')
else:
    print(f'✗ Error: {response.status_code}')
    print(response.content.decode()[:500])
