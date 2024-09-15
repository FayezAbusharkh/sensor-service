from django.urls import path
from .views import ingest_csv, get_median


urlpatterns = [
    path('ingest', ingest_csv, name='ingest_csv'),
    path('median', get_median, name='get_median'),
]
