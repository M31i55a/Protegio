from django.core.mail import send_mail
from django.conf import settings


def send_scan_notification(scan):
    """
    Envoie un email de notification quand un scan est terminé.
    """
    # ← utilise 'success' au lieu de 'status'
    if scan.success:
        statut = '✅ SUCCÈS'
        emoji = '🟢'
    else:
        statut = '❌ ÉCHEC'
        emoji = '🔴'

    nb_vulns = scan.findings_count or 0

    sujet = f"{emoji} NIKTO_SCAN — Scan #{scan.id:04d} terminé — {nb_vulns} vulnérabilité(s) détectée(s)"

    message = f"""
╔══════════════════════════════════════╗
    NIKTO_SCAN — RAPPORT
╚══════════════════════════════════════╝

📋 INFORMATIONS DU SCAN
━━━━━━━━━━━━━━━━━━━━━━
- ID             : #{scan.id:04d}
- Cible          : {scan.target}
- Statut         : {statut}
- Vulnérabilités : {nb_vulns}
- Démarré le     : {scan.started_at}
- Terminé le     : {scan.finished_at}

{"⚠️  DES VULNÉRABILITÉS ONT ÉTÉ DÉTECTÉES !" if nb_vulns > 0 else "✅ Aucune vulnérabilité détectée."}

━━━━━━━━━━━━━━━━━━━━━━
Connecte-toi à NIKTO_SCAN pour voir les détails complets.

— NIKTO_SCAN Automated Scanner
    """

    try:
        send_mail(
            subject=sujet,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFICATION_EMAIL],
            fail_silently=False,
        )
        print(f"[NIKTO_SCAN] Email envoyé pour le scan #{scan.id}")
    except Exception as e:
        print(f"[NIKTO_SCAN] Erreur envoi email : {str(e)}")