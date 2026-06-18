from django.shortcuts import render
from .models import SqlmapScan


def sqlmap_view(request):
    scans = SqlmapScan.objects.all()[:10]
    error = None

    if request.method == 'POST':
        url = request.POST.get('url', '').strip()

        if not url:
            error = 'Veuillez entrer une URL valide'
        else:
            try:
                # Créer une nouvelle analyse SQLMap
                scan = SqlmapScan.objects.create(
                    url=url,
                    status='en cours',
                    result={'message': 'Analyse en cours...'}
                )
                error = None
            except Exception as e:
                error = f'Erreur : {str(e)}'

    context = {
        'scans': scans,
        'error': error,
    }
    return render(request, 'sqlmap/sqlmap.html', context)
