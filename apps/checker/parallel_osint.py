"""
Module optimisé pour les requêtes parallèles - WhatMyName
Utilise ThreadPoolExecutor pour vérifier plusieurs sites en parallèle
"""
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Optimisation des timeouts par catégorie de site
TIMEOUT_BY_CATEGORY = {
    "archived": 3,
    "art": 5,
    "blog": 5,
    "business": 5,
    "coding": 4,
    "dating": 5,
    "finance": 5,
    "gaming": 5,
    "health": 5,
    "hobby": 5,
    "images": 4,
    "misc": 5,
    "music": 5,
    "news": 5,
    "political": 5,
    "search": 4,
    "shopping": 5,
    "social": 4,
    "tech": 4,
    "video": 5,
    "xx NSFW xx": 5
}

def get_site_url(site: Dict, username: str) -> str:
    """Récupère l'URL du site avec le nom d'utilisateur"""
    for key in ["uri_check", "url", "check_uri", "uri"]:
        if key in site and site[key]:
            return site[key].replace("{username}", username)
    return None

def check_username(site: Dict, username: str, timeout: int = None) -> Dict:
    """
    Vérifie si un utilisateur existe sur un site
    Retourne: {name, category, url, exists, status, http_status}
    """
    url = get_site_url(site, username)
    
    if not url:
        return {
            "name": site.get("name"),
            "category": site.get("category", "N/A"),
            "url": None,
            "exists": False,
            "status": "NO_URL",
            "http_status": None
        }
    
    # Déterminer le timeout optimal
    if timeout is None:
        timeout = TIMEOUT_BY_CATEGORY.get(site.get("category"), 5)
    
    try:
        start = time.time()
        resp = requests.get(
            url,
            headers=HEADERS,
            timeout=timeout,
            allow_redirects=True,
            verify=True
        )
        elapsed = time.time() - start
        
        exists = False
        
        # Méthode 1: Vérification par code HTTP
        if site.get("errorType") == "status_code":
            error_code = site.get("errorCode", 404)
            exists = resp.status_code != error_code
        
        # Méthode 2: Vérification par message d'erreur
        elif site.get("errorType") == "message":
            error_msg = site.get("errorMsg", "")
            if error_msg:
                exists = error_msg not in resp.text
            else:
                exists = resp.status_code == 200
        
        # Méthode par défaut
        else:
            exists = resp.status_code == 200
        
        return {
            "name": site.get("name"),
            "category": site.get("category", "N/A"),
            "url": url,
            "exists": exists,
            "status": "FOUND" if exists else "NOT_FOUND",
            "http_status": resp.status_code,
            "elapsed": round(elapsed, 2)
        }
    
    except requests.exceptions.Timeout:
        return {
            "name": site.get("name"),
            "category": site.get("category", "N/A"),
            "url": url,
            "exists": False,
            "status": "TIMEOUT",
            "http_status": None,
            "error": "Timeout"
        }
    
    except requests.exceptions.ConnectionError:
        return {
            "name": site.get("name"),
            "category": site.get("category", "N/A"),
            "url": url,
            "exists": False,
            "status": "ERROR",
            "http_status": None,
            "error": "Connection error"
        }
    
    except Exception as e:
        return {
            "name": site.get("name"),
            "category": site.get("category", "N/A"),
            "url": url,
            "exists": False,
            "status": "ERROR",
            "http_status": None,
            "error": str(e)
        }

def check_username_parallel(sites: List[Dict], username: str, max_workers: int = 20) -> List[Dict]:
    """
    Vérifie les noms d'utilisateur en parallèle sur plusieurs sites
    Retourne les résultats au fur et à mesure (itérateur)
    """
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Soumettre tous les travaux
        futures = {
            executor.submit(check_username, site, username): site 
            for site in sites
        }
        
        # Retourner les résultats au fur et à mesure
        completed = 0
        total = len(futures)
        
        for future in as_completed(futures):
            try:
                result = future.result()
                completed += 1
                result["progress"] = {
                    "completed": completed,
                    "total": total,
                    "percent": round((completed / total) * 100)
                }
                yield result
            except Exception as e:
                completed += 1
                site = futures[future]
                yield {
                    "name": site.get("name"),
                    "category": site.get("category", "N/A"),
                    "url": None,
                    "exists": False,
                    "status": "ERROR",
                    "http_status": None,
                    "error": str(e),
                    "progress": {
                        "completed": completed,
                        "total": total,
                        "percent": round((completed / total) * 100)
                    }
                }
        
        elapsed = time.time() - start_time
        yield {
            "type": "completed",
            "total_time": round(elapsed, 2),
            "sites_checked": total
        }

def check_all_sites(sites: List[Dict], username: str, quick_mode: bool = False) -> Tuple[List[Dict], float]:
    """
    Vérifie rapidement tous les sites (mode rapide)
    Retourne: (résultats, temps_écoulé)
    """
    start_time = time.time()
    results = list(check_username_parallel(sites, username, max_workers=20 if not quick_mode else 10))
    elapsed = time.time() - start_time
    
    return results, elapsed
