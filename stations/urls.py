from django.urls import path
from . import views

urlpatterns = [
    path('', views.station_dashboard, name='station_dashboard'),
    path('inventory/', views.station_inventory, name='station_inventory'),
    path('storage-in/', views.station_storage_in, name='station_storage_in'),
    path('storage-out/<int:inventory_id>/', views.station_storage_out, name='station_storage_out'),
]
