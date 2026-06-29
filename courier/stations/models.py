from django.db import models


class Branch(models.Model):
    """网点"""
    name = models.CharField('网点名称', max_length=100)
    address = models.CharField('地址', max_length=200)
    contact_person = models.CharField('联系人', max_length=50)
    contact_phone = models.CharField('联系电话', max_length=20)
    province = models.CharField('省份', max_length=50)
    city = models.CharField('城市', max_length=50)
    district = models.CharField('区县', max_length=50)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=6, null=True, blank=True)
    open_time = models.TimeField('营业开始时间', default='08:00')
    close_time = models.TimeField('营业结束时间', default='20:00')
    is_active = models.BooleanField('正常营业', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '网点'
        verbose_name_plural = '网点管理'

    def __str__(self):
        return self.name


class Station(models.Model):
    """驿站"""
    name = models.CharField('驿站名称', max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='stations', verbose_name='所属网点')
    address = models.CharField('地址', max_length=200)
    contact_phone = models.CharField('联系电话', max_length=20)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=6, null=True, blank=True)
    open_time = models.TimeField('营业开始时间', default='08:00')
    close_time = models.TimeField('营业结束时间', default='22:00')
    is_active = models.BooleanField('正常营业', default=True)
    pick_code_config = models.CharField('取件码规则', max_length=20, default='phone_last6',
                                       choices=[('phone_last6', '手机号后6位'), ('random_6', '6位随机码'), ('custom', '自定义')])
    max_retention_days = models.IntegerField('最长保管天数', default=3)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '驿站'
        verbose_name_plural = '驿站管理'

    def __str__(self):
        return self.name


class Shelf(models.Model):
    """货架"""
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='shelves', verbose_name='驿站')
    shelf_no = models.CharField('货架编号', max_length=20)
    zone = models.CharField('分区', max_length=10, blank=True, help_text='如A/B/C区或手机尾号分区')
    is_active = models.BooleanField('启用', default=True)

    class Meta:
        verbose_name = '货架'
        verbose_name_plural = '货架管理'
        unique_together = ['station', 'shelf_no']

    def __str__(self):
        return f'{self.station.name} - {self.shelf_no}'


class StationInventory(models.Model):
    """驿站库存表"""
    class InventoryStatus(models.IntegerChoices):
        IN_STORAGE = 0, '在库'
        PICKED_UP = 1, '已取'
        OVERDUE = 2, '滞留'
        RETURNED = 3, '已退回'

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='inventory', verbose_name='订单')
    tracking_id = models.CharField('运单号', max_length=20)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='inventories', verbose_name='驿站')
    shelf = models.ForeignKey(Shelf, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='货架')
    pick_code = models.CharField('取件码', max_length=20)
    storage_time = models.DateTimeField('入库时间', auto_now_add=True)
    out_time = models.DateTimeField('出库时间', null=True, blank=True)
    status = models.IntegerField('库存状态', choices=InventoryStatus.choices, default=InventoryStatus.IN_STORAGE)
    operator = models.CharField('操作人', max_length=50, blank=True)
    receiver_name = models.CharField('取件人姓名', max_length=50, blank=True)
    receiver_phone = models.CharField('取件人电话', max_length=20, blank=True)
    verification_method = models.CharField('验证方式', max_length=20, blank=True,
                                          choices=[('pick_code', '取件码'), ('phone', '手机号'), ('id_card', '身份证')])
    remark = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '驿站库存'
        verbose_name_plural = '驿站库存管理'
        indexes = [
            models.Index(fields=['tracking_id']),
            models.Index(fields=['station', 'status']),
            models.Index(fields=['pick_code']),
        ]

    def __str__(self):
        return f'{self.station.name} - {self.tracking_id} [{self.get_status_display()}]'
