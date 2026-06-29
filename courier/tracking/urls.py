from django.urls import path
from . import views

urlpatterns = [
    path('', views.tracking_search, name='tracking_search'),
    path('<str:tracking_id>/', views.tracking_detail, name='tracking_detail'),
]
