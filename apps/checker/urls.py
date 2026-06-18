from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("results/", views.results, name="results"),
    path("api/search/", views.api_search),
    path("api/search/quick/", views.api_search_quick),
    path("api/check-parallel/", views.api_check_parallel, name="api_check_parallel"),
    path("api/parallel-json/", views.api_parallel_json, name="api_parallel_json"),
]
