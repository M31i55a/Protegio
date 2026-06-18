#!/usr/bin/env python
import requests
import json

url = "http://127.0.0.1:8000/checker/api/check-parallel/?username=john"
print(f"Testing {url}\n")

try:
    r = requests.get(url, stream=True, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Headers: {dict(r.headers)}\n")
    
    if r.status_code == 200:
        count = 0
        for line in r.iter_lines(decode_unicode=True):
            if line and line.startswith('data:'):
                count += 1
                if count <= 5:
                    data = json.loads(line[5:])
                    print(f"Event {count}: {data.get('type')}")
                if count >= 10:
                    break
        print(f"... total events captured: {count}")
    else:
        print(f"\nResponse: {r.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
