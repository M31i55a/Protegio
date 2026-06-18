import subprocess
import os
import json
from datetime import datetime
from django.conf import settings


NIKTO_PATH   = getattr(settings, 'NIKTO_PATH',   r'C:\Strawberry\perl\bin\perl.exe')
NIKTO_SCRIPT = getattr(settings, 'NIKTO_SCRIPT', r'C:\nikto\program\nikto.pl')


def is_nikto_installed():
    """Vérifie que Perl et le script Nikto sont accessibles."""
    return os.path.exists(NIKTO_PATH) and os.path.exists(NIKTO_SCRIPT)


def run_nikto(target, extra_options=None):
    """
    Lance Nikto sur la cible et retourne un dict structuré.
    """
    if not is_nikto_installed():
        return {
            'success': False,
            'error': (
                f"Fichier introuvable : {NIKTO_PATH}. "
                f"Vérifiez NIKTO_PATH et NIKTO_SCRIPT dans settings.py"
            ),
            'output': '',
            'findings': [],
            'started_at': None,
            'finished_at': None,
        }

    # Commande de base
    cmd = [
        NIKTO_PATH,
        NIKTO_SCRIPT,
        '-h', target,
        '-Format', 'json',
        '-nointeractive',
        '-maxtime', '300s',
    ]

    # Options supplémentaires (tuning, port, etc.)
    if extra_options:
        cmd.extend(extra_options)

    started_at = datetime.now().isoformat()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=360,
        )
        finished_at = datetime.now().isoformat()

        output = result.stdout or ''
        stderr = result.stderr or ''

        # Tentative de parse JSON
        findings = []
        try:
            data = json.loads(output)
            # Nikto retourne {"vulnerabilities": [...]}
            if isinstance(data, dict):
                findings = data.get('vulnerabilities', [])
            elif isinstance(data, list):
                findings = data
        except json.JSONDecodeError:
            # Sortie texte brute — on extrait les lignes + (findings)
            findings = []
            for line in output.splitlines():
                line = line.strip()
                if line.startswith('+') and not line.startswith('+ Target') \
                        and 'Nikto' not in line and '-------' not in line:
                    findings.append({'description': line.lstrip('+ ')})

        # Vérifie si le scan a réussi
        success = result.returncode == 0 or len(findings) > 0
        error = None

        if not success:
            error = stderr or output or "Erreur inconnue"
            # Cas particulier : hôte inaccessible
            if 'Unable to connect' in (output + stderr):
                error = f"Impossible de se connecter à {target}. Vérifiez que la cible est accessible."

        return {
            'success':      success,
            'error':        error,
            'output':       output,
            'findings':     findings,
            'started_at':   started_at,
            'finished_at':  finished_at,
        }

    except subprocess.TimeoutExpired:
        return {
            'success':     False,
            'error':       'Timeout — le scan a dépassé 6 minutes.',
            'output':      '',
            'findings':    [],
            'started_at':  started_at,
            'finished_at': datetime.now().isoformat(),
        }
    except FileNotFoundError as e:
        return {
            'success':     False,
            'error':       f"Fichier introuvable : {e}. Vérifiez NIKTO_PATH dans settings.py",
            'output':      '',
            'findings':    [],
            'started_at':  started_at,
            'finished_at': datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            'success':     False,
            'error':       f"Erreur inattendue : {str(e)}",
            'output':      '',
            'findings':    [],
            'started_at':  started_at,
            'finished_at': datetime.now().isoformat(),
        }