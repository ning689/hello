from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
import random, string, datetime

from .models import Order, PaymentRecord
from tracking.models import TrackingLog
from stations.models import Branch


def generate_order_no():
    """生成订单号：日期+6位随机数"""
    date_part = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    rand_part = ''.join(random.choices(string.digits, k=6))
    return f'EX{date_part}{rand_part}'


def generate_tracking_id():
    """生成运单号：SF+13位数字"""
    return f'SF{datetime.datetime.now().strftime("%y%m%d")}{"".join(random.choices(string.digits, k=8))}'


@login_required
def order_create(request):
    """在线寄件"""
    if request.method == 'POST':
        # 基础校验
        required_fields = ['sender_name', 'sender_phone', 'sender_province', 'sender_city', 'sender_district',
                          'sender_address', 'receiver_name', 'receiver_phone', 'receiver_province',
                          'receiver_city', 'receiver_district', 'receiver_address', 'weight', 'goods_type']
        for field in required_fields:
            if not request.POST.get(field):
                messages.error(request, f'请填写完整信息')
                return render(request, 'order_create.html')

        try:
            weight = Decimal(request.POST['weight'])
            if weight <= 0:
                raise ValueError
        except:
            messages.error(request, '请输入有效的重量')
            return render(request, 'order_create.html')

        # 计算运费（简化版）
        freight = weight * Decimal('10') if weight <= 1 else Decimal('10') + (weight - 1) * Decimal('5')
        insurance_fee = Decimal('0')
        is_insured = request.POST.get('is_insured') == 'on'
        if is_insured:
            insured_amount = Decimal(request.POST.get('insured_amount', '0') or '0')
            insurance_fee = insured_amount * Decimal('0.003')
        else:
            insured_amount = Decimal('0')

        total_fee = freight + insurance_fee
        packaging_fee = Decimal(request.POST.get('packaging_fee', '0') or '0')
        total_fee += packaging_fee

        order = Order.objects.create(
            order_no=generate_order_no(),
            tracking_id=generate_tracking_id(),
            sender_name=request.POST['sender_name'],
            sender_phone=request.POST['sender_phone'],
            sender_province=request.POST['sender_province'],
            sender_city=request.POST['sender_city'],
            sender_district=request.POST['sender_district'],
            sender_address=request.POST['sender_address'],
            receiver_name=request.POST['receiver_name'],
            receiver_phone=request.POST['receiver_phone'],
            receiver_province=request.POST['receiver_province'],
            receiver_city=request.POST['receiver_city'],
            receiver_district=request.POST['receiver_district'],
            receiver_address=request.POST['receiver_address'],
            weight=weight,
            goods_type=request.POST['goods_type'],
            goods_desc=request.POST.get('goods_desc', ''),
            is_insured=is_insured,
            insured_amount=insured_amount,
            freight_fee=freight,
            insurance_fee=insurance_fee,
            packaging_fee=packaging_fee,
            total_fee=total_fee,
            express_company='SF',
            user=request.user,
            order_status='waiting_pickup',
        )

        # 创建初始轨迹
        TrackingLog.objects.create(
            order=order,
            tracking_id=order.tracking_id,
            status='created',
            status_desc='订单已创建，等待快递员揽收',
            operator=request.user.username,
            operate_time=timezone.now(),
        )

        messages.success(request, f'下单成功！订单号：{order.order_no}，运单号：{order.tracking_id}')
        return redirect('order_detail', order_id=order.id)

    return render(request, 'order_create.html', {'active_nav': 'order_create'})


@login_required
def order_list(request):
    """我的订单"""
    status_filter = request.GET.get('status', '')
    orders = Order.objects.filter(user=request.user)
    if status_filter:
        orders = orders.filter(order_status=status_filter)
    orders = orders.order_by('-created_at')

    return render(request, 'order_list.html', {
        'orders': orders,
        'current_status': status_filter,
        'active_nav': 'orders',
    })


@login_required
def order_detail(request, order_id):
    """订单详情"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    tracking_logs = TrackingLog.objects.filter(order=order).order_by('-operate_time')
    payments = PaymentRecord.objects.filter(order=order)
    return render(request, 'order_detail.html', {
        'order': order,
        'tracking_logs': tracking_logs,
        'payments': payments,
        'active_nav': 'orders',
    })


@login_required
def order_cancel(request, order_id):
    """取消订单"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.order_status == 'waiting_pickup':
        order.order_status = 'cancelled'
        order.save()
        TrackingLog.objects.create(
            order=order, tracking_id=order.tracking_id, status='cancelled',
            status_desc='订单已取消', operator=request.user.username,
            operate_time=timezone.now(),
        )
        messages.success(request, '订单已取消')
    else:
        messages.error(request, '当前订单状态不可取消')
    return redirect('order_detail', order_id=order.id)
