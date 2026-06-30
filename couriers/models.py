from django.db import models


class CourierProfile(models.Model):
    """快递员拓展信息"""
    VEHICLE_CHOICES = [
        ('electric_bike', '电动车'),
        ('motorcycle', '摩托车'),
        ('truck', '货车'),
        ('on_foot', '步行'),
    ]
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='courier_profile', verbose_name='用户')
    employee_id = models.CharField('工号', max_length=20, unique=True)
    id_card = models.CharField('身份证号', max_length=18)
    vehicle_type = models.CharField('交通工具', max_length=20, choices=VEHICLE_CHOICES, default='electric_bike')
    service_area = models.CharField('服务区域', max_length=200, blank=True, help_text='如：朝阳区-望京街道')
    is_available = models.BooleanField('是否可接单', default=True)
    rating = models.DecimalField('评分', max_digits=3, decimal_places=2, default=5.00)
    total_orders = models.IntegerField('总订单数', default=0)
    total_income = models.DecimalField('总收入', max_digits=12, decimal_places=2, default=0)
    joined_at = models.DateTimeField('入职时间', auto_now_add=True)

    class Meta:
        verbose_name = '快递员信息'
        verbose_name_plural = '快递员管理'

    def __str__(self):
        return f'{self.user.username or self.user.phone} - {self.employee_id}'


class DeliveryTask(models.Model):
    """派送任务"""
    TASK_TYPE_CHOICES = [
        ('pickup', '揽收'),
        ('deliver', '派送'),
    ]
    TASK_STATUS_CHOICES = [
        ('pending', '待处理'),
        ('assigned', '已分配'),
        ('accepted', '已接单'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    courier = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='tasks', verbose_name='快递员')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='delivery_tasks', verbose_name='订单')
    task_type = models.CharField('任务类型', max_length=10, choices=TASK_TYPE_CHOICES)
    status = models.CharField('任务状态', max_length=15, choices=TASK_STATUS_CHOICES, default='pending')
    assigned_at = models.DateTimeField('分配时间', auto_now_add=True)
    accepted_at = models.DateTimeField('接单时间', null=True, blank=True)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)
    route_order = models.IntegerField('路线排序', default=0)
    remark = models.TextField('备注', blank=True)

    class Meta:
        verbose_name = '派送任务'
        verbose_name_plural = '派送任务管理'
        ordering = ['route_order', 'assigned_at']

    def __str__(self):
        return f'{self.get_task_type_display()} - {self.order.order_no} [{self.get_status_display()}]'


class DailyWorkSummary(models.Model):
    """快递员工作日报"""
    courier = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='work_summaries', verbose_name='快递员')
    date = models.DateField('日期')
    pickups = models.IntegerField('揽收数', default=0)
    deliveries = models.IntegerField('派件数', default=0)
    completed = models.IntegerField('已完成', default=0)
    exceptions = models.IntegerField('异常件数', default=0)
    income = models.DecimalField('当日收入', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '工作日报'
        verbose_name_plural = '工作日报管理'
        unique_together = ['courier', 'date']

    def __str__(self):
        return f'{self.courier} - {self.date}'
