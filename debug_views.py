#!/usr/bin/env python
"""Debug checker views errors"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from apps.checker.views import index
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/checker/')

print("Testing index view...")
try:
    response = index(request)
    print(f"✓ Status: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
