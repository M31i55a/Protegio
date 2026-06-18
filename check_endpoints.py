#!/usr/bin/env python
"""Test basic connectivity to checker app"""
import urllib.request
import urllib.error

endpoints = [
    ("Index", "http://127.0.0.1:8000/checker/"),
    ("Results", "http://127.0.0.1:8000/checker/results/"),
    ("API Search", "http://127.0.0.1:8000/checker/api/search/"),
    ("API Parallel", "http://127.0.0.1:8000/checker/api/check-parallel/?username=test"),
]

for name, url in endpoints:
    try:
        req = urllib.request.urlopen(url, timeout=5)
        print(f"✓ {name:20} - {req.status} {req.reason}")
    except urllib.error.HTTPError as e:
        print(f"✗ {name:20} - HTTP {e.code} {e.reason}")
    except Exception as e:
        print(f"✗ {name:20} - {type(e).__name__}: {e}")
