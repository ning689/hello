from django.urls import path
from . import views

urlpatterns = [
    path('', views.address_list, name='address_list'),
    path('add/', views.address_add, name='address_add'),
    path('<int:addr_id>/edit/', views.address_edit, name='address_edit'),
    path('<int:addr_id>/delete/', views.address_delete, name='address_delete'),
]
