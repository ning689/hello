from django.db import models


class Notification(models.Model):
    """通知记录"""
    NOTIFY_CHANNEL = [
        ('sms', '短信'),
        ('wechat', '微信服务通知'),
        ('voice', '语音提醒'),
    ]
    NOTIFY_TYPE = [
        ('pickup_reminder', '取件提醒'),
        ('delivery_notify', '派件通知'),
        ('异常_alert', '异常预警'),
        ('overdue_reminder', '滞留催取'),
        ('status_update', '状态更新'),
    ]
    recipient_phone = models.CharField('接收手机号', max_length=20)
    channel = models.CharField('通知渠道', max_length=10, choices=NOTIFY_CHANNEL)
    notify_type = models.CharField('通知类型', max_length=20, choices=NOTIFY_TYPE)
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    template_id = models.CharField('模板ID', max_length=100, blank=True)
    is_sent = models.BooleanField('已发送', default=False)
    sent_at = models.DateTimeField('发送时间', null=True, blank=True)
    is_read = models.BooleanField('已读', default=False)
    read_at = models.DateTimeField('阅读时间', null=True, blank=True)
    related_order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联订单')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '通知记录'
        verbose_name_plural = '通知记录管理'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient_phone']),
            models.Index(fields=['is_sent']),
        ]

    def __str__(self):
        return f'[{self.get_channel_display()}] {self.title} -> {self.recipient_phone}'


class NotificationTemplate(models.Model):
    """通知模板"""
    name = models.CharField('模板名称', max_length=100)
    channel = models.CharField('通知渠道', max_length=10, choices=Notification.NOTIFY_CHANNEL)
    template_id = models.CharField('厂商模板ID', max_length=100)
    content_template = models.TextField('内容模板', help_text='支持变量：{name}, {pick_code}, {station}, {address}, {time}')
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '通知模板'
        verbose_name_plural = '通知模板管理'

    def __str__(self):
        return f'{self.name} ({self.get_channel_display()})'
