import csv
from collections import Counter
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .utils.detector import scan_url
from .models import ScanResult
import threading
import json

@login_required
def scanner(request):
    result = None
    bulk_results = []

    if request.method == "POST":
        action = request.POST.get("action", "single")

        if action == "single":
            url = request.POST.get("url", "").strip()
            if url:
                result = scan_url(url)
                ScanResult.objects.create(
                    url=result["url"],
                    technologies=result["technologies"],
                    status_code=result.get("status_code"),
                    raw_headers=result.get("headers", {}),
                )

        elif action == "bulk":
            urls_raw = request.POST.get("urls", "")
            urls = [u.strip() for u in urls_raw.splitlines() if u.strip()]
            results_container = [None] * len(urls)

            def scan_thread(index, url):
                res = scan_url(url)
                results_container[index] = res
                ScanResult.objects.create(
                    url=res["url"],
                    technologies=res["technologies"],
                    status_code=res.get("status_code"),
                    raw_headers=res.get("headers", {}),
                )

            threads = []
            for i, url in enumerate(urls):
                t = threading.Thread(target=scan_thread, args=(i, url))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()

            bulk_results = results_container

    history = ScanResult.objects.all()[:10]
    return render(request, "scanner.html", {
        "result": result,
        "bulk_results": bulk_results,
        "history": history,
    })


@login_required
def dashboard(request):
    scans = ScanResult.objects.all()
    total_scans = scans.count()

    tech_counter = Counter()
    category_counter = Counter()

    for scan in scans:
        for tech in scan.technologies:
            tech_counter[tech["name"]] += 1
            category_counter[tech.get("category", "Autre")] += 1

    top_techs = [{"name": k, "count": v} for k, v in tech_counter.most_common(10)]
    top_categories = [{"name": k, "count": v} for k, v in category_counter.most_common(8)]

    return render(request, "dashboard.html", {
        "total_scans": total_scans,
        "total_techs": len(tech_counter),
        "top_techs": json.dumps(top_techs),
        "top_categories": json.dumps(top_categories),
        "recent_scans": scans[:5],
    })


@login_required
def export_csv(request):
    scans = ScanResult.objects.all()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="wappa_results.csv"'
    writer = csv.writer(response)
    writer.writerow(["URL", "Date", "Status HTTP", "Technologies", "Versions"])
    for scan in scans:
        techs = ", ".join([t["name"] for t in scan.technologies])
        versions = ", ".join([f"{t['name']}:{t.get('version','?')}" for t in scan.technologies])
        writer.writerow([scan.url, scan.scanned_at.strftime("%d/%m/%Y %H:%M"), scan.status_code, techs, versions])
    return response


@login_required
def export_pdf(request):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    import io

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Wappa Scanner — Rapport de scan", styles["Title"]))
    elements.append(Spacer(1, 20))

    scans = ScanResult.objects.all()
    data = [["URL", "Date", "HTTP", "Technologies"]]
    for scan in scans:
        techs = ", ".join([
            f"{t['name']} {t.get('version') or ''}" for t in scan.technologies
        ])
        data.append([
            scan.url[:35],
            scan.scanned_at.strftime("%d/%m/%Y %H:%M"),
            str(scan.status_code or "—"),
            techs[:55],
        ])

    table = Table(data, colWidths=[140, 90, 35, 210])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00d4ff")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#1a1a2e"), colors.HexColor("#0f0f1a")]),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2a2a4a")),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="wappa_rapport.pdf"'
    return response


def scan_api(request):
    url = request.GET.get("url", "")
    if not url:
        return JsonResponse({"error": "Paramètre 'url' manquant"}, status=400)
    result = scan_url(url)
    return JsonResponse(result)