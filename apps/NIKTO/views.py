from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Sum
from dateutil import parser as date_parser

from .models import Scan
from .nikto_runner import run_nikto, is_nikto_installed
from .notifications import send_scan_notification  # ← AJOUT


# ─────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────
def dashboard(request):
    """
    Page d'accueil : statistiques globales + 5 derniers scans.
    """
    recent_scans  = Scan.objects.all()[:5]
    total_scans   = Scan.objects.count()
    scans_success = Scan.objects.filter(success=True).count()
    scans_failed  = Scan.objects.filter(success=False).count()
    total_findings = (
        Scan.objects.aggregate(total=Sum('findings_count'))['total'] or 0
    )

    context = {
        'recent_scans':   recent_scans,
        'total_scans':    total_scans,
        'scans_success':  scans_success,
        'scans_failed':   scans_failed,
        'total_findings': total_findings,
        'nikto_ok':       is_nikto_installed(),
    }
    return render(request, 'my_app/dashboard.html', context)


# ─────────────────────────────────────────
#  LANCER UN SCAN
# ─────────────────────────────────────────
def scan_run(request):
    """
    Reçoit le formulaire POST, lance Nikto, sauvegarde le résultat
    et redirige vers le détail du scan.
    """
    if request.method != 'POST':
        return redirect('dashboard')

    target  = request.POST.get('target', '').strip()
    tuning  = request.POST.get('tuning', '').strip()
    port    = request.POST.get('port', '').strip()

    # Validation basique
    if not target:
        messages.error(request, "Veuillez saisir une URL cible.")
        return redirect('dashboard')

    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target

    # Construction des options Nikto supplémentaires
    extra_options = []
    if tuning:
        extra_options += ['-Tuning', tuning]
    if port:
        extra_options += ['-port', port]

    # Lancement du scan
    result = run_nikto(target, extra_options=extra_options if extra_options else None)

    # Sauvegarde en base
    scan = Scan(
        target        = target,
        success       = result['success'],
        error_message = result.get('error'),
        raw_output    = result.get('output', ''),
        tuning        = tuning or None,
        port          = int(port) if port else None,
    )

    # Timestamps
    if result.get('started_at'):
        try:
            scan.started_at = date_parser.parse(result['started_at'])
        except Exception:
            scan.started_at = timezone.now()

    if result.get('finished_at'):
        try:
            scan.finished_at = date_parser.parse(result['finished_at'])
        except Exception:
            scan.finished_at = timezone.now()

    # Findings
    scan.set_findings(result.get('findings', []))
    scan.save()

    # ─── NOTIFICATION EMAIL ───────────────────
    send_scan_notification(scan)  # ← AJOUT
    # ─────────────────────────────────────────

    # Message flash
    if result['success']:
        messages.success(
            request,
            f"Scan terminé — {scan.findings_count} vulnérabilité(s) détectée(s)."
        )
    else:
        messages.error(request, f"Scan échoué : {result.get('error')}")

    return redirect('scan_detail', pk=scan.pk)


# ─────────────────────────────────────────
#  LISTE DES SCANS
# ─────────────────────────────────────────
def scan_list(request):
    """
    Historique paginé avec filtres et recherche.
    """
    queryset = Scan.objects.all()

    # Filtre par statut
    status = request.GET.get('status', '')
    if status == 'success':
        queryset = queryset.filter(success=True)
    elif status == 'failed':
        queryset = queryset.filter(success=False)
    elif status == 'vulns':
        queryset = queryset.filter(findings_count__gt=0)

    # Recherche par cible
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(target__icontains=q)
        )

    # Statistiques globales (sur la sélection filtrée)
    total_findings = (
        queryset.aggregate(total=Sum('findings_count'))['total'] or 0
    )

    # Pagination — 20 scans par page
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page', 1)
    page_obj    = paginator.get_page(page_number)

    context = {
        'scans':          page_obj,
        'page_obj':       page_obj,
        'total_findings': total_findings,
    }
    return render(request, 'my_app/scan_list.html', context)


# ─────────────────────────────────────────
#  DÉTAIL D'UN SCAN
# ─────────────────────────────────────────
def scan_detail(request, pk):
    """
    Affiche les résultats complets d'un scan.
    """
    scan     = get_object_or_404(Scan, pk=pk)
    findings = scan.get_findings()

    context = {
        'scan':     scan,
        'findings': findings,
    }
    return render(request, 'my_app/scan_detail.html', context)


# ─────────────────────────────────────────
#  SUPPRESSION D'UN SCAN
# ─────────────────────────────────────────
def scan_delete(request, pk):
    """
    Supprime un scan après confirmation.
    """
    scan = get_object_or_404(Scan, pk=pk)
    scan.delete()
    messages.success(request, f"Scan #{pk} supprimé.")
    return redirect('scan_list')