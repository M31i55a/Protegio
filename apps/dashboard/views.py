from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# ── PAGE PUBLIQUE (sans authentification) ──
def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'dashboard/landing.html')

# ── DASHBOARD (authentifié) ──
@login_required
def dashboard_home(request):
    apps_by_category = {
        'integrations': [
            {'name':'Nuclei Scanner','icon':'⚙️','desc':'Scan de vulnérabilités','url':'/integrations/nuclei/'},
            {'name':'Port Scanner','icon':'🔌','desc':'Scan des ports','url':'/integrations/portscanner/'},
            {'name':'SSL/TLS Check','icon':'🔒','desc':'Vérification SSL','url':'/integrations/ssl/'},
            {'name':'API Security','icon':'🛡️','desc':'Tests API','url':'/integrations/api/'},
            {'name':'CVE Lookup','icon':'🐛','desc':'Recherche CVE','url':'/integrations/cve/'},
            {'name':'Rapports','icon':'📄','desc':'Rapports PDF','url':'/reports/'},
        ],
        'reconnaissance': [
            {'name':'Whois','icon':'🌐','desc':'Informations domaine','url':'/protegioTools/whois/'},
            {'name':'Whatsmyname','icon':'🔍','desc':'Recherche pseudonymes','url':'/protegioTools/whatsmyname/'},
            {'name':'NsLookup','icon':'📡','desc':'Résolution DNS','url':'/protegioTools/nslookup/'},
            {'name':'DIG-MX Tool','icon':'📬','desc':'Analyse MX','url':'/protegioTools/dig/'},
            {'name':'Harvester','icon':'🎯','desc':'Collecte d\'informations','url':'/havest/'},
            {'name':'Wappalyzer','icon':'🌐','desc':'Détection technologie web','url':'/wappa/'},
        ],
        'scanning': [
            {'name':'OWASP-ZAP','icon':'⚡','desc':'Scanner web','url':'/scanner/zap/'},
            {'name':'NIKTO','icon':'🕷️','desc':'Scan serveur web','url':'/nikto/'},
            {'name':'PerforNet','icon':'📊','desc':'Performance réseau','url':'/perforNet/'},
            {'name':'Burp Suite','icon':'🔀','desc':'Proxy & tests web','url':'/burp-suite/'},
        ],
        'exploitation': [
            {'name':'SQLMap','icon':'💉','desc':'Injection SQL','url':'/sqlmap/'},
        ],
    }

    stats = {
        'total_scans': 3666,
        'vulnerabilities': 42,
        'reports_generated': 156,
        'active_tasks': 8,
        'users_online': 3,
    }

    context = {
        'stats': stats,
        'apps_by_category': apps_by_category,
        'user': request.user,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def api_stats(request):
    stats = {
        'total_scans': 3666,
        'critical_alerts': 42,
        'vulnerabilities': 156,
    }
    return JsonResponse(stats)