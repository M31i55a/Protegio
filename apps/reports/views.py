import os
import json
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.conf import settings


@login_required
def reports_list(request):
    """Display list of all generated reports"""
    
    reports_dir = os.path.join(settings.BASE_DIR, 'reports')
    reports = []
    
    if os.path.exists(reports_dir):
        for filename in sorted(os.listdir(reports_dir), reverse=True):
            if filename.endswith('.html'):
                filepath = os.path.join(reports_dir, filename)
                file_size = os.path.getsize(filepath)
                file_mtime = os.path.getmtime(filepath)
                create_time = datetime.fromtimestamp(file_mtime)
                
                # Extract scan ID from filename
                scan_id = filename.replace('.html', '').replace('zap_report_', '')
                
                reports.append({
                    'filename': filename,
                    'scan_id': scan_id,
                    'created': create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'size': f"{file_size / 1024:.2f} KB",
                    'url': f'/reports/view/{filename}/'
                })
    
    context = {
        'reports': reports,
        'total_reports': len(reports)
    }
    
    return render(request, 'reports/list.html', context)


@login_required
def report_view(request, filename):
    """View a specific report"""
    
    reports_dir = os.path.join(settings.BASE_DIR, 'reports')
    filepath = os.path.join(reports_dir, filename)
    
    # Security: ensure file is in reports directory
    if not filepath.startswith(reports_dir) or not os.path.exists(filepath):
        return JsonResponse({'error': 'Report not found'}, status=404)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return render(request, 'reports/view.html', {'content': content, 'filename': filename})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def report_download(request, filename):
    """Download a report"""
    
    reports_dir = os.path.join(settings.BASE_DIR, 'reports')
    filepath = os.path.join(reports_dir, filename)
    
    # Security: ensure file is in reports directory
    if not filepath.startswith(reports_dir) or not os.path.exists(filepath):
        return JsonResponse({'error': 'Report not found'}, status=404)
    
    try:
        return FileResponse(
            open(filepath, 'rb'),
            as_attachment=True,
            filename=filename
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
