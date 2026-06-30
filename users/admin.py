from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'phone', 'role', 'branch', 'is_staff', 'is_active']
    list_filter = ['role', 'is_active', 'branch']
    search_fields = ['username', 'phone', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('role', 'phone', 'avatar', 'branch')}),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'label', 'name', 'phone', 'is_default']
    list_filter = ['label', 'is_default']
    search_fields = ['name', 'phone', 'detail']
