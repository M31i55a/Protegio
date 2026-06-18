from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_list, name='list'),
    path('view/<str:filename>/', views.report_view, name='view'),
    path('download/<str:filename>/', views.report_download, name='download'),
]
