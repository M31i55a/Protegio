from django.urls import path
from . import views

urlpatterns = [
    path("", views.scanner, name="scanner"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("export/csv/", views.export_csv, name="export_csv"),
    path("export/pdf/", views.export_pdf, name="export_pdf"),
    path("api/scan/", views.scan_api, name="scan_api"),
]