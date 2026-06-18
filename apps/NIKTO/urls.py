 
from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.dashboard,   name='dashboard'),
    path('scan/run/',           views.scan_run,    name='scan_run'),
    path('scans/',              views.scan_list,   name='scan_list'),
    path('scans/<int:pk>/',     views.scan_detail, name='scan_detail'),
    path('scans/<int:pk>/del/', views.scan_delete, name='scan_delete'),
]