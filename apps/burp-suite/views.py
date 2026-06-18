from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Count
import json
import base64
import urllib.parse
import html
import hashlib
import requests
import threading
import time
import os

from .models import (
    ScanTarget, ScanResult, ProxyRequest,
    IntruderPayload, RepeaterRequest, SpiderResult, DecoderData
)

from . import middleware as mw


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────

def dashboard(request):
    stats = {
        'total_scans': ScanTarget.objects.count(),
        'active_scans': ScanTarget.objects.filter(status='running').count(),
        'total_issues': ScanResult.objects.count(),
        'high_issues': ScanResult.objects.filter(severity='high').count(),
        'medium_issues': ScanResult.objects.filter(severity='medium').count(),
        'low_issues': ScanResult.objects.filter(severity='low').count(),
        'proxy_requests': ProxyRequest.objects.count(),
        'spider_urls': SpiderResult.objects.count(),
    }
    recent_scans = ScanTarget.objects.all()[:5]
    recent_issues = ScanResult.objects.select_related('target').all()[:10]
    return render(request, 'burp/dashboard.html', {
        'stats': stats,
        'recent_scans': recent_scans,
        'recent_issues': recent_issues,
        'page': 'dashboard'
    })


# ─────────────────────────────────────────────
# SCANNER
# ─────────────────────────────────────────────

def scanner(request):
    targets = ScanTarget.objects.all()
    return render(request, 'burp/scanner.html', {'targets': targets, 'page': 'scanner'})


@csrf_exempt
@require_http_methods(["POST"])
def start_scan(request):
    data = json.loads(request.body)
    url = data.get('url', '').strip()
    name = data.get('name', url)
    scan_config = data.get('config', {})
    if not url:
        return JsonResponse({'error': 'URL requise'}, status=400)
    target = ScanTarget.objects.create(url=url, name=name, scan_config=scan_config, status='running')
    thread = threading.Thread(target=_run_scan, args=(target.id,))
    thread.daemon = True
    thread.start()
    return JsonResponse({'id': target.id, 'status': 'running', 'message': 'Scan démarré'})


def _run_scan(target_id):
    try:
        target = ScanTarget.objects.get(id=target_id)
        simulated_issues = [
            {'issue_type': 'SQL Injection', 'severity': 'high', 'parameter': 'id',
             'description': 'Injection SQL détectée.', 'evidence': "' OR '1'='1",
             'remediation': 'Utiliser des requêtes paramétrées.'},
            {'issue_type': 'Cross-site Scripting (XSS)', 'severity': 'medium', 'parameter': 'search',
             'description': 'XSS réfléchi détecté.', 'evidence': '<script>alert(1)</script>',
             'remediation': 'Encoder les sorties HTML.'},
            {'issue_type': 'Information Disclosure', 'severity': 'low', 'parameter': '',
             'description': 'Informations sensibles exposées.', 'evidence': 'Server: Apache/2.4.41',
             'remediation': 'Supprimer les en-têtes de version.'},
            {'issue_type': 'Missing Security Headers', 'severity': 'info', 'parameter': '',
             'description': 'En-têtes de sécurité manquants.', 'evidence': 'X-Frame-Options absent',
             'remediation': 'Ajouter les en-têtes de sécurité.'},
        ]
        time.sleep(3)
        for issue in simulated_issues:
            ScanResult.objects.create(
                target=target, url=target.url,
                issue_type=issue['issue_type'], severity=issue['severity'],
                parameter=issue.get('parameter', ''), description=issue['description'],
                evidence=issue['evidence'], remediation=issue['remediation'],
                request_data=f"GET {target.url} HTTP/1.1\nHost: example.com",
                response_data="HTTP/1.1 200 OK\n\n<html>...</html>",
            )
        target.status = 'completed'
        target.save()
    except Exception as e:
        try:
            target = ScanTarget.objects.get(id=target_id)
            target.status = 'failed'
            target.save()
        except Exception:
            pass


@csrf_exempt
def scan_status(request, scan_id):
    target = get_object_or_404(ScanTarget, id=scan_id)
    results = list(target.results.values('id', 'issue_type', 'severity', 'url', 'parameter'))
    return JsonResponse({'status': target.status, 'results_count': len(results), 'results': results})


def scan_detail(request, scan_id):
    target = get_object_or_404(ScanTarget, id=scan_id)
    results = target.results.all()
    severity_counts = results.values('severity').annotate(count=Count('severity'))
    return render(request, 'burp/scan_detail.html', {
        'target': target, 'results': results,
        'severity_counts': severity_counts, 'page': 'scanner'
    })


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_scan(request, scan_id):
    target = get_object_or_404(ScanTarget, id=scan_id)
    target.delete()
    return JsonResponse({'success': True})


# ─────────────────────────────────────────────
# PROXY
# ─────────────────────────────────────────────

def proxy(request):
    requests_qs = ProxyRequest.objects.all()[:100]
    return render(request, 'burp/proxy.html', {'proxy_requests': requests_qs, 'page': 'proxy'})


@csrf_exempt
@require_http_methods(["POST"])
def intercept_request(request):
    data = json.loads(request.body)
    pr = ProxyRequest.objects.create(
        method=data.get('method', 'GET'),
        url=data.get('url', ''),
        host=data.get('host', ''),
        path=data.get('path', '/'),
        request_headers=data.get('headers', {}),
        request_body=data.get('body', ''),
        intercepted=True,
    )
    return JsonResponse({'id': pr.id, 'status': 'intercepted'})


@csrf_exempt
def forward_request(request, req_id):
    pr = get_object_or_404(ProxyRequest, id=req_id)
    try:
        pending_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pending_requests.json')
        forward_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'forward_signal.txt')
        proxy_key = None
        try:
            with open(pending_file, 'r') as f:
                pending = json.load(f)
            for key, entry in pending.items():
                if entry.get('django_id') == req_id:
                    proxy_key = key
                    break
            if not proxy_key and pending:
                proxy_key = list(pending.keys())[0]
        except Exception as e:
            print(f"[Django] Read pending error: {e}")

        if proxy_key:
            with open(forward_file, 'w') as f:
                f.write(proxy_key)
            print(f"[Django] Signal forward ecrit: {proxy_key}")

        pr.intercepted = False
        pr.save()
        return JsonResponse({'status': 'forwarded', 'id': req_id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def drop_request(request, req_id):
    pr = get_object_or_404(ProxyRequest, id=req_id)
    pending_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pending_requests.json')
    drop_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drop_signal.txt')
    proxy_key = None
    try:
        with open(pending_file, 'r') as f:
            pending = json.load(f)
        for key, entry in pending.items():
            if entry.get('django_id') == req_id:
                proxy_key = key
                break
        if not proxy_key and pending:
            proxy_key = list(pending.keys())[0]
    except Exception:
        pass
    if proxy_key:
        with open(drop_file, 'w') as f:
            f.write(proxy_key)
        print(f"[Django] Signal drop ecrit: {proxy_key}")
    pr.delete()
    return JsonResponse({'status': 'dropped'})


def proxy_history(request):
    reqs = ProxyRequest.objects.all().values(
        'id', 'method', 'url', 'host', 'path',
        'request_headers', 'request_body',
        'response_status', 'response_length',
        'response_time', 'timestamp', 'intercepted', 'modified'
    )
    return JsonResponse({'requests': list(reqs)})


@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def clear_proxy_history(request):
    deleted_count, _ = ProxyRequest.objects.all().delete()
    return JsonResponse({'success': True, 'deleted': deleted_count,
                         'message': f'{deleted_count} requête(s) supprimée(s).'})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_proxy_request(request, req_id):
    pr = get_object_or_404(ProxyRequest, id=req_id)
    pr.delete()
    return JsonResponse({'success': True, 'id': req_id})


@csrf_exempt
@require_http_methods(["POST"])
def add_proxy_request(request):
    data = json.loads(request.body)
    pr = ProxyRequest.objects.create(
        method=data.get('method', 'GET'),
        url=data.get('url', ''),
        host=data.get('host', 'example.com'),
        path=data.get('path', '/'),
        request_headers=data.get('headers', {'User-Agent': 'burp_suiteSuite-Django/1.0'}),
        request_body=data.get('body', ''),
        response_status=data.get('response_status', 200),
        response_length=data.get('response_length', 1024),
        response_time=data.get('response_time', 0.45),
    )
    return JsonResponse({'id': pr.id})


# ─────────────────────────────────────────────
# PROXY — INTERCEPT CONTROL
# ─────────────────────────────────────────────

@csrf_exempt
def intercept_toggle(request):
    intercept_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'intercept_state.txt')
    try:
        with open(intercept_file, 'r') as f:
            current = f.read().strip() == 'true'
    except:
        current = False
    new_state = not current
    with open(intercept_file, 'w') as f:
        f.write('true' if new_state else 'false')
    print(f"[Django] Intercept: {new_state}")
    return JsonResponse({'enabled': new_state})


@csrf_exempt
def intercept_status(request):
    intercept_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'intercept_state.txt')
    try:
        with open(intercept_file, 'r') as f:
            enabled = f.read().strip() == 'true'
    except:
        enabled = False
    return JsonResponse({'enabled': enabled})


@csrf_exempt
@require_http_methods(["POST"])
def modify_and_forward(request, req_id):
    pr = get_object_or_404(ProxyRequest, id=req_id)
    try:
        data = json.loads(request.body)
    except Exception:
        data = {}

    if 'body' in data:
        pr.request_body = data['body']
        pr.modified = True
    pr.intercepted = False
    pr.save()

    pending_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pending_requests.json')
    forward_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'forward_signal.txt')

    try:
        with open(pending_file, 'r') as f:
            pending = json.load(f)
        print(f"[Django] pending: {pending}")

        proxy_key = None
        for key, entry in pending.items():
            if entry.get('django_id') == req_id:
                proxy_key = key
                break
        if not proxy_key and pending:
            proxy_key = list(pending.keys())[0]

        print(f"[Django] proxy_key={proxy_key}")

        if proxy_key:
            with open(forward_file, 'w') as f:
                f.write(proxy_key)
            print(f"[Django] Signal forward ecrit: {proxy_key}")
            return JsonResponse({'status': 'forwarded', 'id': req_id})
        else:
            return JsonResponse({'status': 'not_found', 'id': req_id})
    except Exception as e:
        print(f"[Django] Forward error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def release_request(request, req_id):
    pr = get_object_or_404(ProxyRequest, id=req_id)
    pending_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pending_requests.json')
    drop_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drop_signal.txt')
    proxy_key = None
    try:
        with open(pending_file, 'r') as f:
            pending = json.load(f)
        for key, entry in pending.items():
            if entry.get('django_id') == req_id:
                proxy_key = key
                break
        if not proxy_key and pending:
            proxy_key = list(pending.keys())[0]
    except Exception:
        pass
    if proxy_key:
        with open(drop_file, 'w') as f:
            f.write(proxy_key)
    pr.delete()
    return JsonResponse({'status': 'dropped'})


# ─────────────────────────────────────────────
# INTRUDER
# ─────────────────────────────────────────────

def intruder(request):
    payloads = IntruderPayload.objects.all()
    return render(request, 'burp/intruder.html', {'payloads': payloads, 'page': 'intruder'})


@csrf_exempt
@require_http_methods(["POST"])
def run_intruder(request):
    data = json.loads(request.body)
    payload_obj = IntruderPayload.objects.create(
        name=data.get('name', 'Attack'),
        attack_type=data.get('attack_type', 'sniper'),
        target_url=data.get('target_url', ''),
        request_template=data.get('request_template', ''),
        payloads=data.get('payloads', []),
        status='running',
    )
    thread = threading.Thread(target=_run_intruder, args=(payload_obj.id,))
    thread.daemon = True
    thread.start()
    return JsonResponse({'id': payload_obj.id, 'status': 'running'})


def add_payload(request):
    if request.method == "POST":
        payload = request.POST.get("payload")
        print("Payload ajouté :", payload)
    return render(request, 'intruder.html')


def _run_intruder(payload_id):
    try:
        payload_obj = IntruderPayload.objects.get(id=payload_id)
        results = []
        for i, payload in enumerate(payload_obj.payloads[:20]):
            time.sleep(0.1)
            results.append({
                'payload': payload,
                'status': 200 if i % 3 != 0 else 500,
                'length': 1024 + (i * 23),
                'time': round(0.1 + (i * 0.05), 3),
                'interesting': i % 5 == 0,
            })
        payload_obj.results = results
        payload_obj.status = 'completed'
        payload_obj.save()
    except Exception:
        pass


@csrf_exempt
def intruder_status(request, intruder_id):
    obj = get_object_or_404(IntruderPayload, id=intruder_id)
    return JsonResponse({'status': obj.status, 'results': obj.results, 'results_count': len(obj.results)})


# ─────────────────────────────────────────────
# REPEATER
# ─────────────────────────────────────────────

def repeater(request):
    items = RepeaterRequest.objects.all()
    return render(request, 'burp/repeater.html', {'repeater_requests': items, 'page': 'repeater'})


@csrf_exempt
@require_http_methods(["POST"])
def send_repeater(request):
    data = json.loads(request.body)
    req_id = data.get('id')
    if req_id:
        rr = get_object_or_404(RepeaterRequest, id=req_id)
        rr.method = data.get('method', rr.method)
        rr.url = data.get('url', rr.url)
        rr.headers = data.get('headers', rr.headers)
        rr.body = data.get('body', rr.body)
    else:
        rr = RepeaterRequest(
            name=data.get('name', 'Request'),
            method=data.get('method', 'GET'),
            url=data.get('url', ''),
            headers=data.get('headers', {}),
            body=data.get('body', ''),
        )
    try:
        start = time.time()
        resp = requests.request(
            method=rr.method, url=rr.url,
            headers=rr.headers, data=rr.body,
            timeout=15, verify=False,
        )
        elapsed = time.time() - start
        rr.response_status = resp.status_code
        rr.response_headers = dict(resp.headers)
        rr.response_body = resp.text[:50000]
        rr.response_time = round(elapsed, 3)
        rr.history = (rr.history or []) + [{'timestamp': timezone.now().isoformat(),
                                              'method': rr.method, 'url': rr.url,
                                              'response_status': resp.status_code,
                                              'response_time': round(elapsed, 3)}]
        rr.save()
        return JsonResponse({'id': rr.id, 'response_status': resp.status_code,
                             'response_headers': dict(resp.headers),
                             'response_body': resp.text[:50000],
                             'response_time': round(elapsed, 3)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ─────────────────────────────────────────────
# SPIDER
# ─────────────────────────────────────────────

def spider(request):
    targets = ScanTarget.objects.all()
    results = SpiderResult.objects.select_related('target').all()[:200]
    return render(request, 'burp/spider.html', {'targets': targets, 'results': results, 'page': 'spider'})


@csrf_exempt
@require_http_methods(["POST"])
def start_spider(request):
    data = json.loads(request.body)
    url = data.get('url', '').strip()
    if not url:
        return JsonResponse({'error': 'URL requise'}, status=400)
    target, _ = ScanTarget.objects.get_or_create(url=url, defaults={'name': url, 'status': 'running'})
    thread = threading.Thread(target=_run_spider, args=(target.id,))
    thread.daemon = True
    thread.start()
    return JsonResponse({'id': target.id, 'status': 'running'})


def _run_spider(target_id):
    try:
        target = ScanTarget.objects.get(id=target_id)
        base_url = target.url.rstrip('/')
        simulated_urls = [
            (base_url + '/', 200, 'text/html', 45123),
            (base_url + '/login', 200, 'text/html', 12456),
            (base_url + '/api/users', 401, 'application/json', 234),
            (base_url + '/admin', 302, 'text/html', 0),
            (base_url + '/robots.txt', 200, 'text/plain', 456),
        ]
        for url, status, ctype, length in simulated_urls:
            time.sleep(0.3)
            SpiderResult.objects.create(
                target=target, url=url, status_code=status,
                content_type=ctype, content_length=length, parent_url=target.url,
            )
        target.status = 'completed'
        target.save()
    except Exception:
        pass


# ─────────────────────────────────────────────
# DECODER
# ─────────────────────────────────────────────

def decoder(request):
    history = DecoderData.objects.all()[:20]
    return render(request, 'burp/decoder.html', {'history': history, 'page': 'decoder'})


@csrf_exempt
@require_http_methods(["POST"])
def decode_encode(request):
    data = json.loads(request.body)
    input_data = data.get('input', '')
    encoding = data.get('encoding', 'base64')
    operation = data.get('operation', 'decode')
    try:
        if encoding == 'base64':
            output = base64.b64decode(input_data.encode()).decode('utf-8', errors='replace') if operation == 'decode' else base64.b64encode(input_data.encode()).decode()
        elif encoding == 'url':
            output = urllib.parse.unquote(input_data) if operation == 'decode' else urllib.parse.quote(input_data)
        elif encoding == 'html':
            output = html.unescape(input_data) if operation == 'decode' else html.escape(input_data)
        elif encoding == 'hex':
            output = bytes.fromhex(input_data.replace(' ', '')).decode('utf-8', errors='replace') if operation == 'decode' else input_data.encode().hex()
        elif encoding == 'binary':
            if operation == 'decode':
                binary_str = input_data.replace(' ', '')
                output = ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))
            else:
                output = ' '.join(format(ord(c), '08b') for c in input_data)
        elif encoding == 'md5':
            output = hashlib.md5(input_data.encode()).hexdigest()
        elif encoding == 'sha256':
            output = hashlib.sha256(input_data.encode()).hexdigest()
        else:
            output = input_data
        DecoderData.objects.create(input_data=input_data[:1000], output_data=output[:1000],
                                   encoding_type=encoding, operation=operation)
        return JsonResponse({'output': output, 'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e), 'success': False}, status=400)


# ─────────────────────────────────────────────
# COMPARER
# ─────────────────────────────────────────────

def comparer(request):
    return render(request, 'burp/comparer.html', {'page': 'comparer'})


@csrf_exempt
@require_http_methods(["POST"])
def compare_data(request):
    data = json.loads(request.body)
    text1 = data.get('text1', '')
    text2 = data.get('text2', '')
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    diffs = []
    max_lines = max(len(lines1), len(lines2))
    for i in range(max_lines):
        l1 = lines1[i] if i < len(lines1) else ''
        l2 = lines2[i] if i < len(lines2) else ''
        diffs.append({'line': i + 1, 'left': l1, 'right': l2, 'changed': l1 != l2})
    return JsonResponse({'diffs': diffs, 'total_lines': max_lines,
                         'changed_lines': sum(1 for d in diffs if d['changed'])})


# ─────────────────────────────────────────────
# PROXY ACTION
# ─────────────────────────────────────────────

@csrf_exempt
def proxy_action(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        from . import proxy_server
        if action == 'toggle_intercept':
            proxy_server.intercept_enabled = data.get('enabled', False)
            return JsonResponse({'status': 'ok', 'intercept': proxy_server.intercept_enabled})
    return JsonResponse({'error': 'invalid'}, status=400)