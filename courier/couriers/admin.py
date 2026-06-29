from django.contrib import admin
from .models import CourierProfile, DeliveryTask, DailyWorkSummary

@admin.register(CourierProfile)
class CourierProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'vehicle_type', 'is_available', 'rating', 'total_orders']
    list_filter = ['is_available', 'vehicle_type']
    search_fields = ['employee_id', 'user__username', 'user__phone']

@admin.register(DeliveryTask)
class DeliveryTaskAdmin(admin.ModelAdmin):
    list_display = ['courier', 'order', 'task_type', 'status', 'assigned_at', 'completed_at']
    list_filter = ['status', 'task_type']
    search_fields = ['order__order_no', 'courier__username']

@admin.register(DailyWorkSummary)
class DailyWorkSummaryAdmin(admin.ModelAdmin):
    list_display = ['courier', 'date', 'pickups', 'deliveries', 'completed', 'exceptions', 'income']
    list_filter = ['date']
