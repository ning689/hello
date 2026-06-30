from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Station, StationInventory, Shelf
from orders.models import Order
from tracking.models import TrackingLog

@login_required
def station_dashboard(request):
    if request.user.role != 'station_admin':
        messages.error(request, '仅限驿站管理员访问')
        return redirect('home')
    branches = request.user.branch
    stations = Station.objects.filter(branch=branches)
    today = timezone.now().date()
    inventories = StationInventory.objects.filter(station__in=stations)

    return render(request, 'station_dashboard.html', {
        'stations': stations,
        'in_storage': inventories.filter(status=0).count(),
        'today_in': inventories.filter(storage_time__date=today).count(),
        'today_out': inventories.filter(out_time__date=today).count(),
        'overdue': inventories.filter(status=2).count(),
        'active_nav': 'station',
    })

@login_required
def station_inventory(request):
    if request.user.role != 'station_admin':
        messages.error(request, '仅限驿站管理员访问')
        return redirect('home')
    stations = Station.objects.filter(branch=request.user.branch)
    status_filter = request.GET.get('status', '')
    inventories = StationInventory.objects.filter(station__in=stations)
    if status_filter:
        inventories = inventories.filter(status=status_filter)
    inventories = inventories.order_by('-storage_time')

    return render(request, 'station_inventory.html', {
        'inventories': inventories,
        'stations': stations,
        'current_status': status_filter,
        'active_nav': 'station',
    })

@login_required
def station_storage_in(request, inventory_id=None):
    """包裹入库"""
    if request.method == 'POST':
        stations = Station.objects.filter(branch=request.user.branch)
        tracking_id = request.POST.get('tracking_id', '').strip()
        station_id = request.POST.get('station_id')
        shelf_no = request.POST.get('shelf_no', '')

        if not tracking_id:
            messages.error(request, '请输入运单号')
            return redirect('station_inventory')

        order = Order.objects.filter(tracking_id=tracking_id).first()
        if not order:
            messages.error(request, f'未找到运单号 {tracking_id} 对应的订单')
            return redirect('station_inventory')

        if StationInventory.objects.filter(tracking_id=tracking_id, status__in=[0, 2]).exists():
            messages.error(request, '该包裹已在库中')
            return redirect('station_inventory')

        station = Station.objects.get(id=station_id)
        shelf = Shelf.objects.filter(station=station, shelf_no=shelf_no).first() if shelf_no else None

        # 生成取件码
        if station.pick_code_config == 'phone_last6':
            pick_code = order.receiver_phone[-6:] if len(order.receiver_phone) >= 6 else order.receiver_phone
        else:
            import random, string
            pick_code = ''.join(random.choices(string.digits, k=6))

        StationInventory.objects.create(
            order=order,
            tracking_id=tracking_id,
            station=station,
            shelf=shelf,
            pick_code=pick_code,
            operator=request.user.username,
            status=0,
        )

        order.order_status = 'delivering'
        order.save()

        TrackingLog.objects.create(
            order=order, tracking_id=tracking_id, status='arrived_station',
            status_desc=f'包裹已到达{station.name}，取件码：{pick_code}',
            location=station.address, operator=request.user.username,
            operate_time=timezone.now(),
        )

        messages.success(request, f'入库成功！运单号：{tracking_id}，取件码：{pick_code}')
        return redirect('station_inventory')

    stations = Station.objects.filter(branch=request.user.branch)
    return render(request, 'station_storage_in.html', {'stations': stations, 'action': '入库', 'active_nav': 'station'})

@login_required
def station_storage_out(request, inventory_id):
    """包裹出库"""
    inv = get_object_or_404(StationInventory, id=inventory_id)
    if request.method == 'POST':
        pick_code = request.POST.get('pick_code', '')
        if inv.pick_code != pick_code:
            messages.error(request, '取件码错误')
            return redirect('station_inventory')

        inv.status = 1
        inv.out_time = timezone.now()
        inv.receiver_name = request.POST.get('receiver_name', '')
        inv.receiver_phone = request.POST.get('receiver_phone', '')
        inv.verification_method = 'pick_code'
        inv.save()

        order = inv.order
        order.order_status = 'delivered'
        order.sign_time = timezone.now()
        order.save()

        TrackingLog.objects.create(
            order=order, tracking_id=inv.tracking_id, status='delivered',
            status_desc=f'驿站取件签收（{inv.receiver_name}）',
            location=inv.station.address, operator=request.user.username,
            operate_time=timezone.now(),
        )

        messages.success(request, f'出库成功！{inv.tracking_id}')
        return redirect('station_inventory')

    return render(request, 'station_storage_out.html', {'inv': inv})
