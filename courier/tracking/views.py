from django.shortcuts import render
from .models import TrackingLog
from orders.models import Order

def tracking_search(request):
    """物流查询页面"""
    tracking_id = request.GET.get('tracking_id', '')
    logs = None
    order_info = None

    if tracking_id:
        try:
            order = Order.objects.get(tracking_id=tracking_id)
            order_info = order
            logs = TrackingLog.objects.filter(tracking_id=tracking_id).order_by('-operate_time')
        except Order.DoesNotExist:
            logs = None
            order_info = None

    return render(request, 'tracking_search.html', {
        'tracking_id': tracking_id,
        'logs': logs,
        'order': order_info,
        'active_nav': 'tracking',
    })


def tracking_detail(request, tracking_id):
    """物流详情"""
    order = Order.objects.filter(tracking_id=tracking_id).first()
    logs = TrackingLog.objects.filter(tracking_id=tracking_id).order_by('-operate_time')
    return render(request, 'tracking_search.html', {
        'tracking_id': tracking_id,
        'logs': logs,
        'order': order,
        'active_nav': 'tracking',
    })
