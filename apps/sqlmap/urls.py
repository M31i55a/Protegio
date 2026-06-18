from django.urls import path
from .views import sqlmap_view

app_name = 'sqlmap'

urlpatterns = [
    path('', sqlmap_view, name='sqlmap'),
]
