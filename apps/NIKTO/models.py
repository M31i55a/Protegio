from django.db import models
import json


class Scan(models.Model):
    """
    Modèle principal représentant un scan Nikto.
    Stocke la cible, les résultats bruts et les métadonnées.
    """

    # ── Cible ──────────────────────────────────────────────
    target = models.URLField(
        max_length=500,
        verbose_name="URL cible",
        help_text="URL ou IP à scanner (ex: http://192.168.1.1)"
    )

    # ── Statut ─────────────────────────────────────────────
    success = models.BooleanField(
        default=False,
        verbose_name="Succès"
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name="Message d'erreur"
    )

    # ── Résultats ──────────────────────────────────────────
    raw_output = models.TextField(
        blank=True,
        null=True,
        verbose_name="Sortie brute Nikto"
    )
    # Stockage des findings en JSON
    findings_json = models.TextField(
        blank=True,
        null=True,
        verbose_name="Findings JSON"
    )
    findings_count = models.IntegerField(
        default=0,
        verbose_name="Nombre de vulnérabilités"
    )

    # ── Options utilisées ──────────────────────────────────
    tuning = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Tuning Nikto"
    )
    port = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Port"
    )

    # ── Timestamps ─────────────────────────────────────────
    started_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Démarré le"
    )
    finished_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Terminé le"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )

    # ── Durée calculée ─────────────────────────────────────
    @property
    def duration(self):
        """Retourne la durée du scan en secondes."""
        if self.started_at and self.finished_at:
            delta = self.finished_at - self.started_at
            return round(delta.total_seconds(), 1)
        return None

    # ── Findings (sérialisation/désérialisation) ───────────
    def set_findings(self, findings_list):
        """Sauvegarde la liste des findings en JSON."""
        self.findings_json = json.dumps(findings_list, ensure_ascii=False)
        self.findings_count = len(findings_list)

    def get_findings(self):
        """Retourne la liste des findings depuis le JSON."""
        if self.findings_json:
            try:
                return json.loads(self.findings_json)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Scan"
        verbose_name_plural = "Scans"

    def __str__(self):
        return f"Scan #{self.pk} — {self.target} ({'OK' if self.success else 'ERREUR'})"