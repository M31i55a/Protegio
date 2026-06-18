import os
import re

template_dir = r'c:\Users\Harol\Desktop\Unified_tool\unified_tool\apps\burp_suite_suite\templates\burp_suite_suite'

# Regex pour remplacer les références
replacements = [
    (r'{% extends "burp/base.html" %}', r'{% extends "burp_suite_suite/django_base.html" %}'),
    (r'{% include "burp/([^"]+)" %}', r'{% include "burp_suite_suite/\1" %}'),
    (r'{%\s*load\s+static\s*%}', r'{% load static %}'),
]

for filename in os.listdir(template_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {filename} - MODIFIÉ")
        else:
            print(f"- {filename} - Pas de changement")

print("\n✓ CORRECTION COMPLÈTE!")
