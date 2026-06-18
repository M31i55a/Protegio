
import json
import os
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from .forms import UsernameForm
from .parallel_osint import check_username, check_username_parallel
import threading

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "data",
    "wmn-data.json"
)

# Cache pour les données
_data_cache = None
_data_lock = threading.Lock()

def load_data():
    """Charge les données avec cache en mémoire"""
    global _data_cache
    
    if _data_cache is not None:
        return _data_cache
    
    with _data_lock:
        if _data_cache is None:
            with open(DATA_PATH, encoding="utf-8") as f:
                _data_cache = json.load(f)
        return _data_cache

def index(request):
    """Page d'accueil du checker"""
    return render(request, "checker/index.html", {
        "form": UsernameForm()
    })

@require_http_methods(["GET"])
def results(request):
    """Page de résultats avec une liste pré-remplie"""
    form = UsernameForm(request.GET)
    results = []
    found_count = 0
    not_found_count = 0

    if form.is_valid():
        username = form.cleaned_data["username"]
        data = load_data()

        # Limiter à 50 sites pour la première charge
        for site in data["sites"][:50]:
            scan = check_username(site, username)
            results.append(scan)
            if scan.get("exists"):
                found_count += 1
            else:
                not_found_count += 1

    return render(request, "checker/results.html", {
        "form": form,
        "results": results,
        "found_count": found_count,
        "not_found_count": not_found_count
    })

@require_http_methods(["GET"])
def api_check_parallel(request):
    """
    API AJAX qui retourne les résultats au fur et à mesure
    Utilise les requêtes parallèles (ThreadPoolExecutor)
    """
    username = request.GET.get("username", "").strip()
    
    if not username or len(username) < 2:
        return JsonResponse(
            {"error": "Username must be at least 2 characters"},
            status=400
        )
    
    data = load_data()
    
    # Mode streaming pour retourner les résultats au fur et à mesure
    def event_stream():
        results = []
        found_count = 0
        
        for result in check_username_parallel(data["sites"], username, max_workers=20):
            # Résultat de complétude
            if result.get("type") == "completed":
                yield f'data: {json.dumps({"type": "completed", "total_results": len(results), "found": found_count, "total_time": result.get("total_time")})}\n\n'
                break
            
            # Résultat d'une vérification
            if result.get("exists"):
                found_count += 1
            
            results.append({
                "name": result.get("name"),
                "category": result.get("category"),
                "url": result.get("url"),
                "exists": result.get("exists"),
                "status": result.get("status"),
                "http_status": result.get("http_status")
            })
            
            # Envoyer le résultat progressive
            yield f'data: {json.dumps({
                "type": "result",
                "data": result,
                "progress": result.get("progress")
            })}\n\n'
    
    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response

@require_http_methods(["GET"])
def api_search(request):
    """
    API REST qui retourne tous les résultats à la fois (pour compatibilité)
    """
    username = request.GET.get("username", "").strip()
    
    if not username or len(username) < 2:
        return JsonResponse(
            {"error": "Username must be at least 2 characters"},
            status=400
        )
    
    data = load_data()
    results = []
    found_count = 0

    for site in data["sites"]:
        result = check_username(site, username)
        
        # Ne retourner que les sites avec URL
        if result.get("url"):
            results.append(result)
            if result.get("exists"):
                found_count += 1

    return JsonResponse({
        "username": username,
        "found": found_count,
        "not_found": len(results) - found_count,
        "total": len(results),
        "results": results
    })

@require_http_methods(["GET"])
def api_search_quick(request):
    """
    API rapide qui retourne seulement les comptes trouvés
    """
    username = request.GET.get("username", "").strip()
    
    if not username or len(username) < 2:
        return JsonResponse(
            {"error": "Username must be at least 2 characters"},
            status=400
        )
    
    data = load_data()
    results = []

    for site in data["sites"]:
        result = check_username(site, username, timeout=3)  # Timeout court
        
        if result.get("exists") and result.get("url"):
            results.append(result)

    return JsonResponse({
        "username": username,
        "found": len(results),
        "results": results
    })

@require_http_methods(["GET"])
def api_parallel_json(request):
    """
    Parallel search API that returns JSON (non-streaming for better compatibility)
    Uses ThreadPoolExecutor for concurrent site checks
    """
    username = request.GET.get("username", "").strip()
    
    if not username or len(username) < 2:
        return JsonResponse(
            {"error": "Username must be at least 2 characters"},
            status=400
        )
    
    data = load_data()
    results = []
    found_count = 0
    
    # Use parallel processing from parallel_osint
    for result in check_username_parallel(data["sites"], username, max_workers=15):
        # Skip the completion message
        if result.get("type") == "completed":
            break
        
        if result.get("url"):
            results.append(result)
            if result.get("exists"):
                found_count += 1
    
    return JsonResponse({
        "username": username,
        "found": found_count,
        "not_found": len(results) - found_count,
        "total": len(results),
        "results": results
    })
