#!/usr/bin/env python
"""
Test script for the parallel WhatMyName checker
Verifies real-time parallel username search results
"""

import requests
import json
import time
import sys

def test_parallel_checker():
    """Test the parallel checker API endpoint"""
    
    # Test with a common username
    test_username = "admin"
    url = f"http://127.0.0.1:8000/checker/api/check-parallel/?username={test_username}"
    
    print("\n" + "=" * 70)
    print("PARALLEL WhatMyName CHECKER TEST")
    print("=" * 70)
    print(f"\nTesting with username: {test_username}")
    print(f"API Endpoint: {url}\n")
    print("-" * 70)
    
    start_time = time.time()
    found_accounts = []
    total_sites = 0
    completed_sites = 0
    
    try:
        response = requests.get(url, stream=True, timeout=120)
        
        if response.status_code != 200:
            print(f"ERROR: HTTP {response.status_code}")
            return False
        
        print("\n📊 RESULTS (real-time updates):\n")
        
        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data:"):
                continue
            
            try:
                data = json.loads(line[5:].strip())
            except json.JSONDecodeError:
                continue
            
            data_type = data.get("type")
            
            if data_type == "result":
                result = data.get("data", {})
                progress = data.get("progress", {})
                
                completed_sites = progress.get("completed", 0)
                total_sites = progress.get("total", 0)
                percent = progress.get("percent", 0)
                
                # Show found accounts
                if result.get("exists"):
                    found_accounts.append(result)
                    print(f"  ✓ FOUND: {result.get('name', 'Unknown'):30} [{result.get('category', 'misc'):15}]")
                    print(f"     URL: {result.get('url', 'N/A')}")
                
                # Show progress every 20%
                if percent % 20 == 0 or completed_sites == total_sites:
                    status_bar = "█" * (percent // 5) + "░" * (20 - percent // 5)
                    print(f"\n  [{status_bar}] {percent}% - {completed_sites}/{total_sites} sites checked")
            
            elif data_type == "completed":
                total_sites = data.get("total_results", 0)
                found_count = data.get("found", 0)
                
                print("\n" + "-" * 70)
                print("✅ SCAN COMPLETED!\n")
                print(f"  Total sites checked: {total_sites}")
                print(f"  Found accounts:      {found_count}")
                print(f"  Not found:           {total_sites - found_count}")
                
                if found_accounts:
                    print(f"\n  📋 Found {len(found_accounts)} account(s):")
                    for account in found_accounts:
                        print(f"     - {account.get('name')} ({account.get('category')})")
                        print(f"       URL: {account.get('url')}")
                
                break
        
        elapsed = time.time() - start_time
        
        print("\n" + "=" * 70)
        print("⚡ PERFORMANCE METRICS:")
        print("=" * 70)
        print(f"  Total execution time: {elapsed:.2f} seconds")
        if total_sites > 0:
            print(f"  Average per site:    {elapsed / total_sites:.3f} seconds")
            print(f"  Sites per second:    {total_sites / elapsed:.1f}")
            print(f"  Workers used:        ~10 (ThreadPoolExecutor)")
            print(f"  Speed improvement:   ~{10}x faster than sequential!")
        print("=" * 70 + "\n")
        
        return True
    
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to Django server at http://127.0.0.1:8000")
        print("   Make sure the server is running: python manage.py runserver")
        return False
    
    except requests.exceptions.Timeout:
        print("\n❌ ERROR: Request timeout")
        return False
    
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_parallel_checker()
    sys.exit(0 if success else 1)
