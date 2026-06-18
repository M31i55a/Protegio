#!/usr/bin/env python
"""Test if the api_check_parallel view is callable"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from apps.checker import views
from django.test import RequestFactory

print("Checking if api_check_parallel exists...")
if hasattr(views, 'api_check_parallel'):
    print("✓ api_check_parallel is defined")
    
    # Try to call it
    factory = RequestFactory()
    request = factory.get('/checker/api/check-parallel/?username=test')
    
    try:
        response = views.api_check_parallel(request)
        print(f"✓ Function callable - returns {type(response).__name__}")
    except Exception as e:
        print(f"✗ Function error: {e}")
else:
    print("✗ api_check_parallel not found")
    print(f"Available functions: {[name for name in dir(views) if not name.startswith('_')]}")
