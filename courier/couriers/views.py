from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DeliveryTask, CourierProfile, DailyWorkSummary
from orders.models import Order
from tracking.models import TrackingLog

@login_required
def courier_dashboard(request):
    if request.user.role != 'courier':
        messages.error(request, '仅限快递员访问')
        return redirect('home')
    today = timezone.now().date()
    tasks = DeliveryTask.objects.filter(courier=request.user, assigned_at__date=today)
    profile = CourierProfile.objects.filter(user=request.user).first()
    return render(request, 'courier_dashboard.html', {
        'tasks': tasks,
        'profile': profile,
        'pending_count': tasks.filter(status='pending').count(),
        'completed_count': tasks.filter(status='completed').count(),
        'active_nav': 'courier',
    })

@login_required
def courier_tasks(request):
    if request.user.role != 'courier':
        messages.error(request, '仅限快递员访问')
        return redirect('home')
    status_filter = request.GET.get('status', '')
    tasks = DeliveryTask.objects.filter(courier=request.user)
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    tasks = tasks.order_by('-assigned_at')
    return render(request, 'courier_tasks.html', {
        'tasks': tasks,
        'current_status': status_filter,
        'active_nav': 'courier',
    })

@login_required
def courier_task_pickup(request, task_id):
    task = get_object_or_404(DeliveryTask, id=task_id, courier=request.user)
    order = task.order
    if task.task_type == 'pickup' and task.status in ['pending', 'assigned', 'accepted']:
        actual_weight = request.POST.get('actual_weight', order.weight)
        order.order_status = 'picked_up'
        order.courier = request.user
        order.save()
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        TrackingLog.objects.create(
            order=order, tracking_id=order.tracking_id, status='picked_up',
            status_desc=f'快递员{request.user.username}已揽收，实际重量{actual_weight}kg',
            operator=request.user.username, operate_time=timezone.now(),
        )
        messages.success(request, f'揽收成功：{order.order_no}')
    return redirect('courier_tasks')

@login_required
def courier_task_deliver(request, task_id):
    task = get_object_or_404(DeliveryTask, id=task_id, courier=request.user)
    order = task.order
    if task.task_type == 'deliver' and task.status in ['pending', 'assigned', 'accepted', 'in_progress']:
        order.order_status = 'delivered'
        order.sign_time = timezone.now()
        order.save()
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        TrackingLog.objects.create(
            order=order, tracking_id=order.tracking_id, status='delivered',
            status_desc=f'已签收（快递员{request.user.username}）',
            location=order.receiver_address,
            operator=request.user.username, operate_time=timezone.now(),
        )
        messages.success(request, f'签收成功：{order.order_no}')
    return redirect('courier_tasks')

@login_required
def courier_report_anomaly(request, task_id):
    task = get_object_or_404(DeliveryTask, id=task_id, courier=request.user)
    if request.method == 'POST':
        from anomalies.models import AnomalyTicket
        order = task.order
        order.order_status = 'exception'
        order.save()
        ticket = AnomalyTicket.objects.create(
            ticket_no=f'AT{timezone.now().strftime("%Y%m%d%H%M%S")}',
            order=order,
            source='courier_report',
            anomaly_type=request.POST.get('anomaly_type', 'other'),
            description=request.POST.get('description', ''),
            priority='medium',
            reporter=request.user,
        )
        TrackingLog.objects.create(
            order=order, tracking_id=order.tracking_id, status='exception',
            status_desc=f'异常上报：{ticket.get_anomaly_type_display()}',
            operator=request.user.username, operate_time=timezone.now(),
        )
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        messages.success(request, f'异常已上报，工单号：{ticket.ticket_no}')
        return redirect('courier_tasks')
    return render(request, 'courier_report_anomaly.html', {'task': task})
