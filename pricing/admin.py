from django.contrib import admin
from .models import FreightTemplate, FreightRule, InsuranceRate

class FreightRuleInline(admin.TabularInline):
    model = FreightRule
    extra = 1

@admin.register(FreightTemplate)
class FreightTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'express_company', 'mode', 'first_price', 'effective_date', 'is_active']
    list_filter = ['is_active', 'express_company', 'mode']
    inlines = [FreightRuleInline]

@admin.register(FreightRule)
class FreightRuleAdmin(admin.ModelAdmin):
    list_display = ['template', 'province', 'city', 'first_price_override', 'surcharge', 'is_remote_area']
    list_filter = ['is_remote_area', 'province']

@admin.register(InsuranceRate)
class InsuranceRateAdmin(admin.ModelAdmin):
    list_display = ['min_amount', 'max_amount', 'rate', 'is_active']
