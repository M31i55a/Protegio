#!/usr/bin/env python
"""List all registered URLs"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.urls import get_resolver

resolver = get_resolver()

print("Checking URLs for checker app:\n")
for pattern in resolver.url_patterns:
    print(f"Pattern: {pattern.pattern}")
    if hasattr(pattern, 'url_patterns'):
        for subpattern in pattern.url_patterns:
            print(f"  └─ {subpattern.pattern}")
