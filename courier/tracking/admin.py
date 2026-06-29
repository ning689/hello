from django.contrib import admin
from .models import TrackingLog

@admin.register(TrackingLog)
class TrackingLogAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'status_desc', 'location', 'operator', 'operate_time']
    list_filter = ['status', 'operate_time']
    search_fields = ['tracking_id', 'status_desc']
