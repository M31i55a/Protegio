#!/usr/bin/env python
"""
Script de configuration initiale pour OAuth
Exécutez ceci après les migrations pour configurer les bases
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.contrib.sites.models import Site
from django.conf import settings

def setup_initial_site():
    """Configure le site Django initial"""
    try:
        # Obtenir ou créer le site
        site = Site.objects.get(pk=settings.SITE_ID)
        print(f"✓ Site existant trouvé: {site.name} ({site.domain})")
    except Site.DoesNotExist:
        site = Site.objects.create(
            id=settings.SITE_ID,
            name='PROTEGIO',
            domain='localhost:8000'
        )
        print(f"✓ Nouveau site créé: {site.name} ({site.domain})")
        print("  Note: Mettez à jour le domaine dans l'admin après le déploiement")

def print_oauth_setup_instructions():
    """Affiche les instructions de configuration OAuth"""
    print("\n" + "="*60)
    print("Configuration OAuth requise")
    print("="*60)
    
    providers = [
        {
            'name': 'Google',
            'url': 'https://console.cloud.google.com/',
            'docs': 'https://developers.google.com/identity/protocols/oauth2'
        },
        {
            'name': 'Microsoft',
            'url': 'https://portal.azure.com/',
            'docs': 'https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app'
        },
        {
            'name': 'GitHub',
            'url': 'https://github.com/settings/developers',
            'docs': 'https://docs.github.com/en/developers/apps/building-oauth-apps'
        }
    ]
    
    for i, provider in enumerate(providers, 1):
        print(f"\n{i}. {provider['name']}")
        print(f"   Console: {provider['url']}")
        print(f"   Docs: {provider['docs']}")
        print(f"   Redirect URI: http://localhost:8000/accounts/{provider['name'].lower()}/login/callback/")
    
    print("\n" + "="*60)
    print("Ensuite, allez sur http://localhost:8000/admin/")
    print("Accédez à: Social applications > Add Social application")
    print("="*60 + "\n")

if __name__ == '__main__':
    print("\n🔧 Configuration initiale de l'authentification PROTEGIO\n")
    
    setup_initial_site()
    print_oauth_setup_instructions()
    
    print("✓ Configuration initiale terminée!")
    print("\nProchaines étapes:")
    print("1. Configurez vos applications OAuth (Google, Microsoft, GitHub)")
    print("2. Allez sur l'admin Django: http://localhost:8000/admin/")
    print("3. Ajoutez vos Social applications")
    print("4. Testez l'authentification sur http://localhost:8000/accounts/signup/")
