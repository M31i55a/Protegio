import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist

# Essayer de charger le template directement
try:
    tmpl = loader.get_template('dashboard/dashboard.html')
    print(f"✓ Template trouvé: {tmpl.origin}")
except TemplateDoesNotExist as e:
    print(f"✗ Template non trouvé: {e}")
except Exception as e:
    print(f"✗ Erreur: {e}")
