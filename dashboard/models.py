from django.db import models


class DailyStats(models.Model):
    """每日运营统计"""
    date = models.DateField('日期', unique=True)
    total_orders = models.IntegerField('总订单数', default=0)
    pickup_count = models.IntegerField('揽收量', default=0)
    delivery_count = models.IntegerField('签收量', default=0)
    in_transit_count = models.IntegerField('运输中', default=0)
    exception_count = models.IntegerField('异常量', default=0)
    cancelled_count = models.IntegerField('取消量', default=0)
    pending_pickup_count = models.IntegerField('待揽收', default=0)
    revenue = models.DecimalField('营收', max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '每日统计'
        verbose_name_plural = '运营数据统计'
        ordering = ['-date']

    def __str__(self):
        return f'{self.date} 订单:{self.total_orders} 营收:¥{self.revenue}'


class BranchDailyStats(models.Model):
    """网点每日统计"""
    branch = models.ForeignKey('stations.Branch', on_delete=models.CASCADE, related_name='daily_stats', verbose_name='网点')
    date = models.DateField('日期')
    total_orders = models.IntegerField('订单数', default=0)
    pickup_count = models.IntegerField('揽收量', default=0)
    delivery_count = models.IntegerField('派送量', default=0)
    exception_count = models.IntegerField('异常量', default=0)
    revenue = models.DecimalField('营收', max_digits=15, decimal_places=2, default=0)
    on_time_rate = models.DecimalField('准时率(%)', max_digits=5, decimal_places=2, default=100.00)

    class Meta:
        verbose_name = '网点统计'
        verbose_name_plural = '网点统计管理'
        unique_together = ['branch', 'date']
        ordering = ['-date']

    def __str__(self):
        return f'{self.branch.name} {self.date}'


class OperationLog(models.Model):
    """操作日志审计"""
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='操作人')
    action = models.CharField('操作', max_length=100)
    target_type = models.CharField('操作对象类型', max_length=50)
    target_id = models.CharField('操作对象ID', max_length=50, blank=True)
    detail = models.TextField('详情', blank=True)
    ip_address = models.CharField('IP地址', max_length=50, blank=True)
    created_at = models.DateTimeField('操作时间', auto_now_add=True)

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志审计'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.action} @ {self.created_at}'
