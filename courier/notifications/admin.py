from django.contrib import admin
from .models import Notification, NotificationTemplate

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient_phone', 'channel', 'notify_type', 'is_sent', 'is_read', 'created_at']
    list_filter = ['channel', 'notify_type', 'is_sent', 'is_read']

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel', 'template_id', 'is_active']
