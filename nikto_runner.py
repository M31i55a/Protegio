import subprocess
import json
import os
import tempfile
from datetime import datetime

# ============================================================
# CHEMINS VERS NIKTO
# ============================================================
PERL_PATH  = r"C:\Strawberry\perl\bin\perl.exe"
NIKTO_PATH = r"C:\Strawberry\perl\bin\nikto.bat"
# ============================================================


def run_nikto(target_url, extra_options=None):
    """
    Lance un scan Nikto sur l'URL cible et retourne les résultats.
    """
    tmp_dir = os.path.expanduser('~')
    tmp_fd, tmp_path = tempfile.mkstemp(suffix='.json', dir=tmp_dir)
    os.close(tmp_fd)

    started_at = datetime.now().isoformat()

    try:
        cmd = [
            NIKTO_PATH,
            '-h', target_url,
            '-Format', 'json',
            '-output', tmp_path,
            '-nointeractive',
            '-Tuning', '123456789abc',
            '-timeout', '3',
            '-maxtime', '600',
        ]

        if extra_options:
            cmd.extend(extra_options)

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=660,
        )

        finished_at = datetime.now().isoformat()
        raw_output  = process.stdout + process.stderr

        # ── Détection d'un échec de connexion ──────────────────────────
        if '[FAIL]' in raw_output or 'Unable to connect' in raw_output:
            return {
                'success':     False,
                'output':      raw_output,
                'findings':    [],
                'started_at':  started_at,
                'finished_at': finished_at,
                'error':       'Impossible de se connecter à la cible.',
            }

        # ── Parsing des résultats ───────────────────────────────────────
        findings = []

        if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
            with open(tmp_path, 'r', encoding='utf-8') as f:
                try:
                    nikto_data = json.load(f)
                    findings   = parse_nikto_json(nikto_data)
                except json.JSONDecodeError:
                    pass  # on tombe sur le fallback texte ci-dessous

        # ── CORRECTION BUG : fallback texte toujours exécuté si JSON vide ──
        # Le JSON de Nikto peut être valide mais ne contenir aucune vuln
        # alors que la sortie texte en contient. On fusionne les deux.
        text_findings = parse_nikto_text(raw_output)

        # Fusionner : on garde les findings JSON + ceux du texte non dupliqués
        existing_msgs = {f['msg'] for f in findings}
        for tf in text_findings:
            if tf['msg'] not in existing_msgs:
                findings.append(tf)
                existing_msgs.add(tf['msg'])

        return {
            'success':     True,
            'output':      raw_output,
            'findings':    findings,
            'started_at':  started_at,
            'finished_at': finished_at,
            'error':       None,
        }

    except subprocess.TimeoutExpired:
        finished_at = datetime.now().isoformat()
        return {
            'success':     False,
            'output':      '',
            'findings':    [],
            'started_at':  started_at,
            'finished_at': finished_at,
            'error':       'Le scan a dépassé le délai de 5 minutes.',
        }

    except FileNotFoundError as e:
        finished_at = datetime.now().isoformat()
        return {
            'success':     False,
            'output':      '',
            'findings':    [],
            'started_at':  started_at,
            'finished_at': finished_at,
            'error':       (
                f'Fichier introuvable : {str(e)}. '
                f'Vérifiez NIKTO_PATH="{NIKTO_PATH}"'
            ),
        }

    except Exception as e:
        finished_at = datetime.now().isoformat()
        return {
            'success':     False,
            'output':      '',
            'findings':    [],
            'started_at':  started_at,
            'finished_at': finished_at,
            'error':       f'Erreur inattendue : {str(e)}',
        }

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def parse_nikto_json(data):
    """
    Parse le JSON produit par Nikto 2.6.
    Structure : { "host": [ { "vulnerabilities": [...] } ] }
    """
    findings        = []
    vulnerabilities = []

    if isinstance(data, dict) and 'host' in data:
        host_data = data['host']
        if isinstance(host_data, list):
            for host in host_data:
                vulnerabilities.extend(host.get('vulnerabilities', []))
        elif isinstance(host_data, dict):
            vulnerabilities = host_data.get('vulnerabilities', [])
    elif isinstance(data, list):
        vulnerabilities = data
    elif isinstance(data, dict) and 'vulnerabilities' in data:
        vulnerabilities = data['vulnerabilities']

    for vuln in vulnerabilities:
        if not isinstance(vuln, dict):
            continue

        msg = (
            vuln.get('msg')
            or vuln.get('message')
            or vuln.get('description')
            or ''
        ).strip()

        if not msg:
            continue

        findings.append({
            'id':     vuln.get('id', 'N/A'),
            'osvdb':  str(vuln.get('OSVDB', vuln.get('osvdb', ''))).strip() or 'N/A',
            'method': (vuln.get('method') or 'GET').upper(),
            'url':    vuln.get('url', '/') or '/',
            'msg':    msg,
        })

    return findings


def parse_nikto_text(output):
    """
    Parser sur la sortie texte de Nikto.

    CORRECTION : on inclut maintenant TOUTES les lignes utiles,
    y compris les headers manquants [013587], versions obsolètes
    [600050], [600595], [600625] et vulnérabilités comme XST [000434].

    Seules les lignes purement techniques (IP, port, timing) sont ignorées.
    """
    import re
    findings = []

    # Uniquement les infos de connexion brutes — PAS les vulnérabilités
    SKIP_EXACT_PREFIXES = (
        'Target IP:',
        'Target Hostname:',
        'Target Port:',
        'Start Time:',
        'End Time:',
        'Nikto v',
        '0 host(s) tested',
        'No CGI Directories',   # info technique, pas une vuln
    )

    # ── CORRECTION : on ne filtre PLUS "Platform:", "Server:" etc.
    # car ils peuvent contenir des infos de version utiles.

    seen_msgs = set()  # éviter les doublons

    for line in output.splitlines():
        line = line.strip()
        if not line.startswith('+ '):
            continue

        msg = line[2:].strip()

        # Ignorer les lignes purement de connexion
        if any(msg.startswith(p) for p in SKIP_EXACT_PREFIXES):
            continue

        # Ignorer les [FAIL]
        if '[FAIL]' in msg:
            continue

        # ── Extraire l'URL si présente (/path: description)
        url = '/'
        url_match = re.match(r'^(/[^\s:]*)\s*:\s+(.+)', msg)
        if url_match:
            url = url_match.group(1)
            msg = url_match.group(2).strip()

        # ── Extraire l'ID entre crochets [013587]
        finding_id = 'N/A'
        id_match   = re.match(r'^\[(\w+)\]\s+(.*)', msg)
        if id_match:
            finding_id = id_match.group(1)
            msg        = id_match.group(2).strip()

        # ── Extraire OSVDB si présent
        osvdb = 'N/A'
        osvdb_match = re.search(r'OSVDB-(\d+)', msg)
        if osvdb_match:
            osvdb = osvdb_match.group(1)

        # ── Détecter la méthode HTTP si mentionnée dans le message
        method = 'GET'
        method_match = re.search(r'\b(GET|POST|PUT|DELETE|TRACE|OPTIONS|HEAD)\b', msg)
        if method_match:
            method = method_match.group(1)

        if msg and msg not in seen_msgs:
            seen_msgs.add(msg)
            findings.append({
                'id':     finding_id,
                'osvdb':  osvdb,
                'method': method,
                'url':    url,
                'msg':    msg,
            })

    return findings


def is_nikto_installed():
    try:
        result = subprocess.run(
            [NIKTO_PATH, '-Version'],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0 or 'nikto' in result.stdout.lower()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False