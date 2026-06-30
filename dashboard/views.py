from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum
from datetime import timedelta, date
from orders.models import Order
from dashboard.models import DailyStats, BranchDailyStats
from anomalies.models import AnomalyTicket
from stations.models import Branch, StationInventory

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, '仅限管理员访问')
        return redirect('home')

    today = timezone.now().date()
    month_start = today.replace(day=1)

    # 核心指标
    total_orders = Order.objects.count()
    today_orders = Order.objects.filter(created_at__date=today).count()
    pending = Order.objects.filter(order_status='waiting_pickup').count()
    in_transit = Order.objects.filter(order_status='in_transit').count()
    delivered = Order.objects.filter(order_status='delivered').count()
    exception = Order.objects.filter(order_status='exception').count()
    total_revenue = Order.objects.aggregate(s=Sum('total_fee'))['s'] or 0
    today_revenue = Order.objects.filter(created_at__date=today).aggregate(s=Sum('total_fee'))['s'] or 0

    # 按状态分布
    status_data = {
        'pending': pending,
        'picked_up': Order.objects.filter(order_status='picked_up').count(),
        'in_transit': in_transit,
        'delivering': Order.objects.filter(order_status='delivering').count(),
        'delivered': delivered,
        'exception': exception,
        'cancelled': Order.objects.filter(order_status='cancelled').count(),
    }

    # 本月每日数据
    daily_stats = DailyStats.objects.filter(date__gte=month_start).order_by('-date')[:30]

    # 最近订单
    recent_orders = Order.objects.all().order_by('-created_at')[:15]

    # 异常工单
    pending_tickets = AnomalyTicket.objects.filter(status='pending').count()
    recent_tickets = AnomalyTicket.objects.all().order_by('-report_time')[:5]

    # 网点排行
    branch_stats = BranchDailyStats.objects.filter(date=today).order_by('-revenue')[:10]

    branches = Branch.objects.annotate(order_count=Count('stations__inventories')).order_by('-order_count')

    return render(request, 'admin_dashboard.html', {
        'total_orders': total_orders,
        'today_orders': today_orders,
        'pending': pending,
        'in_transit': in_transit,
        'delivered': delivered,
        'exception': exception,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'status_data': status_data,
        'daily_stats': daily_stats,
        'recent_orders': recent_orders,
        'pending_tickets': pending_tickets,
        'recent_tickets': recent_tickets,
        'branches': branches,
        'active_nav': 'admin',
    })
