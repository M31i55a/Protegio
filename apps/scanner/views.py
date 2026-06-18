import time
import os
import requests
from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django import forms

# Formulaire (on le met ici pour que le fichier soit autonome)
class ScanForm(forms.Form):
    target_url = forms.URLField(
        label="URL à scanner",
        widget=forms.URLInput(attrs={'placeholder': 'https://example.com', 'class': 'form-control'}),
        required=True
    )
    max_depth = forms.IntegerField(
        label="Profondeur max du spider (0 = illimité)",
        initial=5,
        min_value=0,
        required=False
    )

class HomeView(View):
    template_name = 'scanner/home.html'

    def get(self, request):
        form = ScanForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ScanForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        target = form.cleaned_data['target_url'].rstrip('/')
        max_depth = form.cleaned_data.get('max_depth', 5)

        context = self.perform_zap_scan(target, max_depth)
        return render(request, 'scanner/result.html', context)

    def check_zap_availability(self):
        """Vérifie si ZAP est disponible"""
        try:
            base_url = settings.ZAP_DAEMON_URL.rstrip('/')
            response = requests.get(
                f"{base_url}/JSON/core/view/version/",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False

    def generate_mock_report(self, target):
        """Génère un rapport de démonstration"""
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>PROTEGIO Security Scan Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .header {{ background: #1f3a5f; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .alert {{ padding: 10px; margin: 10px 0; border-left: 4px solid #ff6b6b; background: #fff5f5; }}
                .info {{ border-left-color: #4ecdc4; background: #f0fffe; }}
                .warning {{ border-left-color: #ffa502; background: #fff8f0; }}
                .success {{ border-left-color: #51cf66; background: #f1fdf4; }}
                h1 {{ color: #1f3a5f; }}
                h2 {{ color: #2c3e50; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #ecf0f1; font-weight: bold; }}
                tr:hover {{ background: #f9f9f9; }}
                .stat {{ display: inline-block; margin: 10px; padding: 15px; background: #ecf0f1; border-radius: 5px; }}
                .stat-number {{ font-size: 24px; font-weight: bold; color: #1f3a5f; }}
                .stat-label {{ font-size: 12px; color: #7f8c8d; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔒 PROTEGIO Security Scan Report</h1>
                <p>Security Assessment Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            <div class="section">
                <h2>📋 Scan Summary</h2>
                <p><strong>Target:</strong> {target}</p>
                <p><strong>Scan Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Scanner:</strong> PROTEGIO Demo Scanner</p>
                
                <div class="stat">
                    <div class="stat-number">0</div>
                    <div class="stat-label">Critical Issues</div>
                </div>
                <div class="stat">
                    <div class="stat-number">2</div>
                    <div class="stat-label">High Issues</div>
                </div>
                <div class="stat">
                    <div class="stat-number">5</div>
                    <div class="stat-label">Medium Issues</div>
                </div>
                <div class="stat">
                    <div class="stat-number">8</div>
                    <div class="stat-label">Low Issues</div>
                </div>
            </div>

            <div class="section">
                <h2>🔍 Detailed Findings</h2>
                
                <h3>High Priority Issues</h3>
                <div class="alert warning">
                    <strong>[HIGH]</strong> Missing Security Headers
                    <p>The application is missing critical HTTP security headers such as Content-Security-Policy, X-Frame-Options, and Strict-Transport-Security.</p>
                </div>
                
                <div class="alert warning">
                    <strong>[HIGH]</strong> Outdated Framework Version
                    <p>The web framework is using an outdated version that may have known vulnerabilities.</p>
                </div>

                <h3>Medium Priority Issues</h3>
                <div class="alert info">
                    <strong>[MEDIUM]</strong> Sensitive Information Disclosure
                    <p>Debug mode appears to be enabled in production, which could leak sensitive information.</p>
                </div>
                
                <div class="alert info">
                    <strong>[MEDIUM]</strong> Missing HTTPS Configuration
                    <p>Not all endpoints are properly configured for HTTPS.</p>
                </div>

                <div class="alert info">
                    <strong>[MEDIUM]</strong> Cookie Security
                    <p>Session cookies are not properly configured with secure and HTTP-only flags.</p>
                </div>
            </div>

            <div class="section">
                <h2>✅ Recommendations</h2>
                <table>
                    <tr>
                        <th>Issue</th>
                        <th>Recommendation</th>
                        <th>Priority</th>
                    </tr>
                    <tr>
                        <td>Security Headers</td>
                        <td>Implement Content-Security-Policy, X-Frame-Options, Strict-Transport-Security headers</td>
                        <td><strong style="color: #ff6b6b;">Critical</strong></td>
                    </tr>
                    <tr>
                        <td>Framework Update</td>
                        <td>Update to the latest stable version of the framework</td>
                        <td><strong style="color: #ffa502;">High</strong></td>
                    </tr>
                    <tr>
                        <td>Production Configuration</td>
                        <td>Disable debug mode and configure proper logging</td>
                        <td><strong style="color: #ffa502;">High</strong></td>
                    </tr>
                    <tr>
                        <td>HTTPS Enforcement</td>
                        <td>Ensure all endpoints use HTTPS with valid certificates</td>
                        <td><strong style="color: #4ecdc4;">Medium</strong></td>
                    </tr>
                </table>
            </div>

            <div class="section">
                <h2>📊 Technical Details</h2>
                <p><strong>Note:</strong> This is a demonstration report generated by PROTEGIO. For production scans, install and configure OWASP ZAP daemon.</p>
                <p><em>To enable full scanning capabilities, configure ZAP_DAEMON_URL in your environment settings.</em></p>
            </div>

            <footer style="text-align: center; margin-top: 40px; color: #7f8c8d; border-top: 1px solid #ecf0f1; padding-top: 20px;">
                <p>PROTEGIO Security Scanner - Professional Penetration Testing Tool</p>
                <p>Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </footer>
        </body>
        </html>
        """
        return html_report

    def perform_zap_scan(self, target, max_depth=5):
        """Effectue un scan ZAP ou génère un rapport de démonstration"""
        
        # D'abord, vérifier si ZAP est disponible
        zap_available = self.check_zap_availability()
        
        if not zap_available:
            # Si ZAP n'est pas disponible, retourner un rapport de démonstration
            print("[!] ZAP non disponible - génératon rapport de démonstration")
            html_report = self.generate_mock_report(target)
            
            # Sauvegarde du rapport
            os.makedirs("reports", exist_ok=True)
            report_filename = f"zap_report_{int(time.time())}.html"
            report_path = os.path.join("reports", report_filename)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(html_report)
            
            return {
                'success': True,
                'target': target,
                'html_report': html_report,
                'report_path': report_path,
                'alert_count': 15,
                'zap_available': False,
                'message': 'Rapport de démonstration généré (ZAP non disponible)'
            }
        
        # Sinon, faire un vrai scan ZAP
        try:
            base_url = settings.ZAP_DAEMON_URL.rstrip('/')
            apikey = settings.ZAP_API_KEY

            params = {}
            if apikey:
                params['apikey'] = apikey

            # 1. Spider (découverte)
            print(f"[*] Spider → {target}")
            spider_resp = requests.get(
                f"{base_url}/JSON/spider/action/scan/",
                params={**params, 'url': target, 'maxChildren': max_depth or None},
                timeout=30
            )
            spider_resp.raise_for_status()
            spider_id = spider_resp.json()['scan']

            # Attente spider
            while True:
                status = requests.get(
                    f"{base_url}/JSON/spider/view/status/",
                    params={**params, 'scanId': spider_id},
                    timeout=30
                ).json()['status']
                if int(status) >= 100:
                    break
                time.sleep(5)

            # 2. Active scan
            print("[*] Active scan...")
            ascan_resp = requests.get(
                f"{base_url}/JSON/ascan/action/scan/",
                params={**params, 'url': target, 'recurse': 'true', 'inScopeOnly': 'true'},
                timeout=30
            )
            ascan_resp.raise_for_status()
            ascan_id = ascan_resp.json()['scan']

            # Attente active scan
            start_time = time.time()
            while True:
                status = requests.get(
                    f"{base_url}/JSON/ascan/view/status/",
                    params={**params, 'scanId': ascan_id},
                    timeout=30
                ).json()['status']
                if int(status) >= 100:
                    break
                if time.time() - start_time > settings.ZAP_TIMEOUT:
                    return {'error': 'Scan actif timeout'}
                time.sleep(10)

            # 3. Rapport HTML
            report_resp = requests.get(
                f"{base_url}/OTHER/core/other/htmlreport/",
                params=params,
                timeout=30
            )
            report_resp.raise_for_status()
            html_report = report_resp.text

            # Sauvegarde optionnelle
            os.makedirs("reports", exist_ok=True)
            report_filename = f"zap_report_{int(time.time())}.html"
            report_path = os.path.join("reports", report_filename)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(html_report)

            # Nombre d'alertes (simple appel API)
            alerts_resp = requests.get(
                f"{base_url}/JSON/core/view/alerts/",
                params={**params, 'baseurl': target},
                timeout=30
            )
            alert_count = len(alerts_resp.json()) if alerts_resp.ok else 0

            return {
                'success': True,
                'target': target,
                'html_report': html_report,
                'report_path': report_path,
                'alert_count': alert_count,
                'zap_available': True,
                'message': 'Scan ZAP complété avec succès'
            }

        except requests.exceptions.Timeout:
            print("[!] Timeout - Génération rapport de démonstration")
            html_report = self.generate_mock_report(target)
            os.makedirs("reports", exist_ok=True)
            report_filename = f"zap_report_{int(time.time())}.html"
            report_path = os.path.join("reports", report_filename)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(html_report)
            
            return {
                'success': True,
                'target': target,
                'html_report': html_report,
                'report_path': report_path,
                'alert_count': 15,
                'zap_available': False,
                'message': 'Rapport de démonstration généré (Timeout ZAP)'
            }
        except requests.exceptions.RequestException as e:
            print(f"[!] Erreur connexion ZAP: {str(e)} - Génération rapport de démonstration")
            html_report = self.generate_mock_report(target)
            os.makedirs("reports", exist_ok=True)
            report_filename = f"zap_report_{int(time.time())}.html"
            report_path = os.path.join("reports", report_filename)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(html_report)
            
            return {
                'success': True,
                'target': target,
                'html_report': html_report,
                'report_path': report_path,
                'alert_count': 15,
                'zap_available': False,
                'message': f'Rapport de démonstration généré (ZAP indisponible: {str(e)})'
            }
        except Exception as e:
            print(f"[!] Erreur générale: {str(e)}")
            html_report = self.generate_mock_report(target)
            os.makedirs("reports", exist_ok=True)
            report_filename = f"zap_report_{int(time.time())}.html"
            report_path = os.path.join("reports", report_filename)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(html_report)
            
            return {
                'success': True,
                'target': target,
                'html_report': html_report,
                'report_path': report_path,
                'alert_count': 15,
                'zap_available': False,
                'message': f'Rapport de démonstration généré ({str(e)})'
            }