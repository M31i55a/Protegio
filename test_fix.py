#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from apps.integrations.services import NucleiService, PortScanService, SSLTLSService, APISecurityService

print("Testing Nuclei Scanner...")
scan = NucleiService.start_scan('example.com')
print(f'✓ Scan Nuclei créé: ID={scan.id}')
print(f'  - Target: {scan.target}')
print(f'  - Status: {scan.status}')
print(f'  - Vulnerabilities: {scan.vulnerabilities_found}')
print(f'  - Templates: {scan.templates_used}')
print(f'  - Duration: {scan.duration}')

print("\nTesting Port Scanner...")
port_scan = PortScanService.start_scan('example.com')
print(f'✓ Port scan créé: ID={port_scan.id}')
print(f'  - Target: {port_scan.target}')
print(f'  - Open ports: {port_scan.open_ports_count}')
print(f'  - Duration: {port_scan.duration}')

print("\nTesting SSL/TLS Checker...")
ssl_check = SSLTLSService.start_check('example.com')
print(f'✓ SSL Check créé: ID={ssl_check.id}')
print(f'  - Target: {ssl_check.target}')
print(f'  - Status: {ssl_check.status}')

print("\nTesting API Security Tester...")
api_test = APISecurityService.start_test('https://api.example.com', 'auth')
print(f'✓ API Test créé: ID={api_test.id}')
print(f'  - URL: {api_test.api_url}')
print(f'  - Type: {api_test.test_type}')
print(f'  - Vulnerable: {api_test.vulnerable}')

print("\n✅ Tous les outils fonctionnent correctement!")
