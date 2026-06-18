#!/usr/bin/env python
"""Test URL routing"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.urls import reverse
from django.test import Client

# Test if the URL exists
print("Testing URL routing...")

client = Client()

# Test the parallel endpoint
response = client.get('/checker/api/check-parallel/?username=test')
print(f"GET /checker/api/check-parallel/?username=test")
print(f"  Status: {response.status_code}")

# Test if reverse works
try:
    url = reverse('api_check_parallel')
    print(f"  Reverse url: {url}")
except Exception as e:
    print(f"  Reverse error: {e}")

# Test the index
response = client.get('/checker/')
print(f"\nGET /checker/")
print(f"  Status: {response.status_code}")
