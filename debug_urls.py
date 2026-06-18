#!/usr/bin/env python
"""Debug the 404 issue"""
import requests
import json

def test_url(url, description, stream=False):
    print(f"\nTesting: {description} (stream={stream})")
    print(f"URL: {url}")
    
    try:
        r = requests.get(url, stream=stream, timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Final URL: {r.url}")
        
        if r.status_code == 200:
            print("✓ Success!")
        else:
            print(f"✗ Error: {r.status_code}")
            if 'not found' in r.text.lower():
                print("  (Page not found)")
    except Exception as e:
        print(f"✗ Exception: {type(e).__name__}: {e}")

# Test API with different stream settings
test_url('http://127.0.0.1:8000/checker/api/check-parallel/?username=test', 'API (stream=False)', False) 
test_url('http://127.0.0.1:8000/checker/api/check-parallel/?username=test', 'API (stream=True)', True)
