from django.urls import path
from . import views

urlpatterns = [
    path('', views.courier_dashboard, name='courier_dashboard'),
    path('tasks/', views.courier_tasks, name='courier_tasks'),
    path('tasks/<int:task_id>/pickup/', views.courier_task_pickup, name='courier_task_pickup'),
    path('tasks/<int:task_id>/deliver/', views.courier_task_deliver, name='courier_task_deliver'),
    path('tasks/<int:task_id>/report-anomaly/', views.courier_report_anomaly, name='courier_report_anomaly'),
]
