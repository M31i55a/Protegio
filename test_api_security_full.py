#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client
from apps.integrations.services import APISecurityService

# Create some test data first
print("Creating test data...")
test1 = APISecurityService.start_test('https://api.example.com', 'auth')
test2 = APISecurityService.start_test('https://api.other.com', 'cors')
print(f"✓ Created {test1.id} and {test2.id}")

# Now test the endpoint
client = Client()
response = client.get('/integrations/api-security/')
print(f'\nHTTP Status: {response.status_code}')

if response.status_code == 200:
    print('✓ Page API Security loaded successfully!')
    content = response.content.decode()
    
    # Check for the correct URL
    if 'integrations:api_test_detail' in content:
        print('✓ Correct URL name found in template!')
    else:
        print('✗ URL name not found in template')
    
    # Check for test data
    if test1.api_url in content:
        print('✓ Test data is displayed!')
    else:
        print('⚠ Test data might not be displayed')
else:
    print(f'✗ Error: {response.status_code}')
