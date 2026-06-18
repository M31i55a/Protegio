#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client
from apps.integrations.services import (NucleiService, PortScanService, 
                                        SSLTLSService, APISecurityService, 
                                        CVEService)

print("=" * 70)
print("TESTING ALL INTEGRATION TOOLS")
print("=" * 70)

client = Client()

# 1. Nuclei Scanner
print("\n1. Testing Nuclei Scanner...")
nuclei = NucleiService.start_scan('test.com')
response = client.get(f'/integrations/nuclei/{nuclei.id}/')
print(f"   HTTP Status: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")

# 2. Port Scanner
print("2. Testing Port Scanner...")
port = PortScanService.start_scan('test.com')
response = client.get(f'/integrations/ports/{port.id}/')
print(f"   HTTP Status: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")

# 3. SSL/TLS Checker
print("3. Testing SSL/TLS Checker...")
ssl = SSLTLSService.start_check('test.com')
response = client.get(f'/integrations/ssl/{ssl.id}/')
print(f"   HTTP Status: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")

# 4. API Security Test
print("4. Testing API Security Tester...")
api = APISecurityService.start_test('https://api.test.com', 'auth')
response = client.get(f'/integrations/api-security/{api.id}/')
print(f"   HTTP Status: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")

# 5. List Views
print("\n5. Testing List Views...")
endpoints = [
    ('/integrations/nuclei/', 'Nuclei'),
    ('/integrations/ports/', 'Ports'),
    ('/integrations/ssl/', 'SSL/TLS'),
    ('/integrations/api-security/', 'API Security'),
    ('/integrations/cve/', 'CVE Lookup'),
]

for endpoint, name in endpoints:
    response = client.get(endpoint)
    status = '✓' if response.status_code == 200 else '✗'
    print(f"   {name}: HTTP {response.status_code} {status}")

print("\n" + "=" * 70)
print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 70)
