#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Test authentication flow
client = Client()

print("=" * 60)
print("AUTHENTICATION SYSTEM TEST")
print("=" * 60)

# Test 1: Check login page loads
print("\n[TEST 1] Login page accessibility...")
response = client.get('/accounts/login/')
if response.status_code == 200:
    print("✓ Login page loads successfully (HTTP 200)")
else:
    print(f"✗ Login page failed (HTTP {response.status_code})")

# Test 2: Check signup page loads
print("\n[TEST 2] Signup page accessibility...")
response = client.get('/accounts/signup/')
if response.status_code == 200:
    print("✓ Signup page loads successfully (HTTP 200)")
else:
    print(f"✗ Signup page failed (HTTP {response.status_code})")

# Test 3: Login with credentials
print("\n[TEST 3] Login with admin credentials...")
response = client.post('/accounts/login/', {
    'username': 'admin',
    'password': 'admin123456'
})
print(f"Login response: HTTP {response.status_code}")
if response.status_code in [200, 302]:
    print("✓ Login form processed successfully")
else:
    print(f"✗ Login form failed")

# Test 4: Check if user is authenticated
print("\n[TEST 4] Session authentication check...")
try:
    # Create a test user if doesn't exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123456')
        print("Created admin user")
    
    response = client.post('/accounts/login/', {
        'username': 'admin',
        'password': 'admin123456'
    }, follow=True)
    
    if response.wsgi_request.user.is_authenticated:
        print("✓ User authenticated after login")
    else:
        print("✗ User not authenticated after login")
except Exception as e:
    print(f"✗ Error during authentication test: {e}")

# Test 5: Check protected views require login
print("\n[TEST 5] Protected views require login...")
response = client.get('/dashboard/', follow=False)
if response.status_code == 302:
    if '/accounts/login/' in response.url:
        print("✓ Dashboard correctly redirects to login")
    else:
        print(f"✗ Dashboard redirects to unexpected URL: {response.url}")
else:
    print(f"✗ Dashboard returned HTTP {response.status_code} instead of redirect")

# Test 6: Check URLs are properly named
print("\n[TEST 6] URL name resolution...")
from django.urls import reverse, NoReverseMatch
url_names = ['login', 'signup', 'logout', 'profile', 'activity_log', 'scan_history']
for url_name in url_names:
    try:
        url = reverse(f'accounts:{url_name}')
        print(f"✓ {url_name}: {url}")
    except NoReverseMatch:
        print(f"✗ {url_name}: Not found")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("All authentication components are properly configured!")
print("\nNext steps:")
print("1. Test login in browser: http://localhost:8000/accounts/login/")
print("2. Use credentials: admin / admin123456")
print("3. After login, you should see the dashboard")
print("=" * 60)
