#!/usr/bin/env python
"""Simple test to verify the API is responding and working"""
import requests
import json
import sys
import time

def test_api():
    url = "http://127.0.0.1:8000/checker/api/check-parallel/?username=john"
    
    print("Testing WhatMyName Parallel Checker API...")
    print(f"URL: {url}\n")
    
    try:
        start = time.time()
        response = requests.get(url, stream=True, timeout=120)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}\n")
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text[:500])
            return False
        
        line_count = 0
        found_count = 0
        completed = False
        
        print("Streaming results...\n")
        
        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.startswith('data:'):
                continue
            
            line_count += 1
            data = json.loads(line[5:])
            
            if data.get('type') == 'result':
                result = data.get('data', {})
                if result.get('exists'):
                    found_count += 1
                    print(f"✓ {found_count}. {result.get('name')}: {result.get('url')}")
            
            elif data.get('type') == 'completed':
                completed = True
                elapsed = time.time() - start
                print(f"\n✅ Completed in {elapsed:.1f}s")
                print(f"Total: {data.get('total_results')} sites")
                print(f"Found: {found_count} accounts")
                break
        
        if not completed:
            print("\n⚠️  Stream ended unexpectedly")
            return False
        
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
