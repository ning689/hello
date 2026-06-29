from django.contrib import admin
from .models import AnomalyTicket, Complaint

@admin.register(AnomalyTicket)
class AnomalyTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_no', 'order', 'anomaly_type', 'priority', 'status', 'reporter', 'assignee', 'report_time']
    list_filter = ['status', 'priority', 'anomaly_type', 'source']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'complaint_type', 'status', 'created_at']
    list_filter = ['status', 'complaint_type']
