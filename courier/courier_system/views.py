from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta, date
from orders.models import Order
from dashboard.models import DailyStats


def home(request):
    """首页看板"""
    now = timezone.now()
    today = now.date()
    week_ago = today - timedelta(days=7)

    context = {
        'active_nav': 'home',
    }

    if request.user.is_authenticated:
        if request.user.role == 'admin':
            # 管理员看全局
            today_stats = DailyStats.objects.filter(date=today).first()
            week_orders = Order.objects.filter(created_at__gte=week_ago).count()
            total_orders = Order.objects.count()
            pending_orders = Order.objects.filter(order_status='waiting_pickup').count()
            in_transit = Order.objects.filter(order_status='in_transit').count()
            delivered = Order.objects.filter(order_status='delivered').count()
            exception = Order.objects.filter(order_status='exception').count()

            context.update({
                'today_stats': today_stats,
                'week_orders': week_orders,
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'in_transit': in_transit,
                'delivered': delivered,
                'exception': exception,
                'recent_orders': Order.objects.all().order_by('-created_at')[:10],
            })
        elif request.user.role == 'courier':
            from couriers.models import DeliveryTask
            tasks_today = DeliveryTask.objects.filter(
                courier=request.user,
                assigned_at__date=today
            )
            context.update({
                'pending_tasks': tasks_today.filter(status='pending').count(),
                'today_tasks': tasks_today.filter(status='completed').count(),
                'total_tasks': tasks_today.count(),
                'recent_tasks': tasks_today.order_by('-assigned_at')[:5],
            })
        elif request.user.role == 'station_admin':
            from stations.models import StationInventory, Station
            stations = Station.objects.filter(branch=request.user.branch)
            context.update({
                'in_storage': StationInventory.objects.filter(station__in=stations, status=0).count(),
                'today_in': StationInventory.objects.filter(station__in=stations, storage_time__date=today).count(),
                'overdue': StationInventory.objects.filter(station__in=stations, status=2).count(),
            })
        else:
            # C端用户看自己的订单
            user_orders = Order.objects.filter(user=request.user)
            context.update({
                'my_orders': user_orders.order_by('-created_at')[:5],
                'order_counts': {
                    s: user_orders.filter(order_status=s).count()
                    for s in ['waiting_pickup', 'in_transit', 'delivered', 'exception']
                },
            })

    return render(request, 'home.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'欢迎回来，{user.username}！')
            return redirect('home')
        messages.error(request, '用户名或密码错误')
    return render(request, 'login.html', {'active_nav': 'login'})


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        from users.models import User
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        role = request.POST.get('role', 'user')
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
        elif User.objects.filter(phone=phone).exists():
            messages.error(request, '手机号已注册')
        else:
            user = User.objects.create_user(username=username, password=password, phone=phone, role=role)
            login(request, user)
            messages.success(request, '注册成功！')
            return redirect('home')
    return render(request, 'register.html', {'active_nav': 'register'})
