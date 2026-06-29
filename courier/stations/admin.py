from django.contrib import admin
from .models import Branch, Station, Shelf, StationInventory

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'contact_person', 'contact_phone', 'is_active']
    list_filter = ['is_active', 'city']
    search_fields = ['name', 'contact_phone']

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'contact_phone', 'is_active', 'max_retention_days']
    list_filter = ['is_active', 'branch']
    search_fields = ['name', 'contact_phone']

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ['station', 'shelf_no', 'zone', 'is_active']
    list_filter = ['station', 'is_active']

@admin.register(StationInventory)
class StationInventoryAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'station', 'shelf', 'pick_code', 'status', 'storage_time', 'out_time']
    list_filter = ['status', 'storage_time', 'station']
    search_fields = ['tracking_id', 'pick_code', 'receiver_phone']
