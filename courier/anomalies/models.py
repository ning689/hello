from django.db import models


class AnomalyTicket(models.Model):
    """异常工单"""
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    ]
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('resolved', '已解决'),
        ('closed', '已关闭'),
    ]
    SOURCE_CHOICES = [
        ('courier_report', '快递员上报'),
        ('user_complaint', '用户投诉'),
        ('system_alert', '系统预警'),
    ]
    ANOMALY_TYPE_CHOICES = [
        ('wrong_address', '地址错误'),
        ('cant_reach', '联系不上'),
        ('package_damaged', '包裹破损'),
        ('rejected', '拒收退回'),
        ('out_of_area', '超区无法派送'),
        ('lost', '包裹丢失'),
        ('delayed', '滞留超时'),
        ('other', '其他'),
    ]

    ticket_no = models.CharField('工单编号', max_length=32, unique=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='anomaly_tickets', verbose_name='关联订单')
    source = models.CharField('来源', max_length=20, choices=SOURCE_CHOICES)
    anomaly_type = models.CharField('异常类型', max_length=20, choices=ANOMALY_TYPE_CHOICES)
    description = models.TextField('问题描述')
    images = models.TextField('图片凭证', blank=True, help_text='JSON数组存储图片URL')
    priority = models.CharField('优先级', max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField('工单状态', max_length=15, choices=STATUS_CHOICES, default='pending')
    reporter = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='reported_tickets', verbose_name='上报人')
    assignee = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets', verbose_name='处理人')
    handler_remark = models.TextField('处理备注', blank=True)
    resolution = models.TextField('处理结果', blank=True)
    report_time = models.DateTimeField('上报时间', auto_now_add=True)
    handle_time = models.DateTimeField('处理时间', null=True, blank=True)
    close_time = models.DateTimeField('关闭时间', null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '异常工单'
        verbose_name_plural = '异常工单管理'
        ordering = ['-report_time']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['anomaly_type']),
        ]

    def __str__(self):
        return f'{self.ticket_no} - {self.get_anomaly_type_display()} [{self.get_status_display()}]'


class Complaint(models.Model):
    """用户投诉"""
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='complaints', verbose_name='关联订单')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='complaints', verbose_name='投诉人')
    complaint_type = models.CharField('投诉类型', max_length=20, choices=[
        ('delayed', '配送延迟'), ('damaged', '包裹破损'), ('lost', '快件丢失'),
        ('service', '服务态度'), ('wrong_delivery', '错送'), ('other', '其他'),
    ])
    description = models.TextField('投诉内容')
    status = models.CharField('状态', max_length=10, choices=[
        ('pending', '待处理'), ('processing', '处理中'), ('resolved', '已解决'), ('closed', '已关闭'),
    ], default='pending')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    resolved_at = models.DateTimeField('解决时间', null=True, blank=True)

    class Meta:
        verbose_name = '用户投诉'
        verbose_name_plural = '投诉管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} 投诉 {self.order} - {self.get_complaint_type_display()}'
