from django.contrib import admin
from .models import Order, PaymentRecord


class PaymentRecordInline(admin.TabularInline):
    model = PaymentRecord
    extra = 0
    readonly_fields = ['pay_no', 'pay_type', 'amount', 'pay_status', 'pay_time']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'tracking_id', 'sender_name', 'receiver_name', 'order_status', 'total_fee', 'created_at']
    list_filter = ['order_status', 'pay_status', 'express_company', 'created_at']
    search_fields = ['order_no', 'tracking_id', 'sender_phone', 'receiver_phone']
    readonly_fields = ['order_no', 'created_at', 'update_time']
    inlines = [PaymentRecordInline]
    fieldsets = (
        ('订单信息', {'fields': ('order_no', 'tracking_id', 'order_status', 'express_company')}),
        ('寄件人', {'fields': ('sender_name', 'sender_phone', 'sender_province', 'sender_city', 'sender_district', 'sender_address')}),
        ('收件人', {'fields': ('receiver_name', 'receiver_phone', 'receiver_province', 'receiver_city', 'receiver_district', 'receiver_address')}),
        ('包裹信息', {'fields': ('weight', 'volume', 'length', 'width', 'height', 'goods_type', 'goods_desc', 'is_insured', 'insured_amount')}),
        ('费用', {'fields': ('freight_fee', 'insurance_fee', 'packaging_fee', 'total_fee', 'pay_type', 'pay_status', 'pay_time')}),
        ('服务', {'fields': ('pick_up_time', 'packaging_method', 'is_collect_on_delivery', 'cod_amount')}),
        ('关联', {'fields': ('user', 'courier', 'branch', 'remark')}),
        ('签收', {'fields': ('sign_image', 'sign_photo', 'sign_time')}),
    )


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ['pay_no', 'order', 'pay_type', 'amount', 'pay_status', 'pay_time']
    list_filter = ['pay_type', 'pay_status']
    search_fields = ['pay_no', 'order__order_no']
