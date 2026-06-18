import shutil
import os
from pathlib import Path

# Define source and destination mappings
copies = [
    # burp_suite Suite templates
    ('c:\\Users\\Harol\\Desktop\\Unified_tool\\burp_suite_suite\\templates\\burp_suite',
     'c:\\Users\\Harol\\Desktop\\Unified_tool\\unified_tool\\apps\\burp_suite_suite\\templates\\burp_suite_suite'),
    
    # Nikto templates
    ('c:\\Users\\Harol\\Desktop\\Unified_tool\\Nikto\\templates\\mon_app',
     'c:\\Users\\Harol\\Desktop\\Unified_tool\\unified_tool\\apps\\nikto\\templates\\nikto'),
    
    # SQLMap templates
    ('c:\\Users\\Harol\\Desktop\\Unified_tool\\Sqlmap-app\\scanner\\templates\\scanner',
     'c:\\Users\\Harol\\Desktop\\Unified_tool\\unified_tool\\apps\\sqlmap\\templates\\sqlmap'),
]

print("=" * 80)
print("COPIE DES TEMPLATES".center(80))
print("=" * 80 + "\n")

for src, dst in copies:
    print(f"\nSource: {src}")
    print(f"Destination: {dst}")
    
    if os.path.exists(src):
        # Create destination directory if it doesn't exist
        os.makedirs(dst, exist_ok=True)
        
        # Copy all files from source to destination
        for filename in os.listdir(src):
            src_file = os.path.join(src, filename)
            dst_file = os.path.join(dst, filename)
            
            # Skip directories, copy only files
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dst_file)
                print(f"  ✓ Copié: {filename}")
            elif os.path.isdir(src_file) and filename != '__pycache__':
                # Recursively copy subdirectories
                if os.path.exists(dst_file):
                    shutil.rmtree(dst_file)
                shutil.copytree(src_file, dst_file)
                print(f"  ✓ Dossier copié: {filename}/")
        
        print(f"  ✓ Copie terminée!")
    else:
        print(f"  ✗ Source non trouvée!")

print("\n" + "=" * 80)
print("✓ COPIE COMPLÈTE!".center(80))
print("=" * 80 + "\n")
