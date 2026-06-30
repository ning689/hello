from django.db import models


class TrackingLog(models.Model):
    """物流轨迹表"""
    STATUS_CHOICES = [
        ('created', '已创建'),
        ('waiting_pickup', '待揽收'),
        ('picked_up', '已揽收'),
        ('in_transit', '运输中'),
        ('arrived_station', '到达驿站'),
        ('delivering', '派送中'),
        ('delivered', '已签收'),
        ('exception', '异常'),
        ('returned', '已退回'),
    ]

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='tracking_logs', verbose_name='订单')
    tracking_id = models.CharField('运单号', max_length=20, db_index=True)
    status = models.CharField('状态码', max_length=20, choices=STATUS_CHOICES)
    status_desc = models.CharField('状态描述', max_length=100)
    location = models.CharField('当前位置', max_length=200, blank=True)
    operator = models.CharField('操作人', max_length=50, blank=True)
    operate_time = models.DateTimeField('操作时间')
    remark = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '物流轨迹'
        verbose_name_plural = '物流轨迹管理'
        ordering = ['-operate_time']
        indexes = [
            models.Index(fields=['tracking_id']),
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return f'{self.tracking_id} - {self.status_desc} @ {self.operate_time}'
