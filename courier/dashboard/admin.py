from django.contrib import admin
from .models import DailyStats, BranchDailyStats, OperationLog

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_orders', 'pickup_count', 'delivery_count', 'exception_count', 'revenue']
    list_filter = ['date']

@admin.register(BranchDailyStats)
class BranchDailyStatsAdmin(admin.ModelAdmin):
    list_display = ['branch', 'date', 'total_orders', 'revenue', 'on_time_rate']
    list_filter = ['date', 'branch']

@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'target_type', 'target_id', 'created_at']
    list_filter = ['action', 'target_type', 'created_at']
