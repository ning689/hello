from django.db import models


class Order(models.Model):
    """订单主表 - 对应PRD express_order表"""
    class OrderStatus(models.TextChoices):
        WAITING_PICKUP = 'waiting_pickup', '待揽收'
        PICKED_UP = 'picked_up', '已揽收'
        IN_TRANSIT = 'in_transit', '运输中'
        DELIVERING = 'delivering', '派送中'
        DELIVERED = 'delivered', '已签收'
        EXCEPTION = 'exception', '异常'
        CANCELLED = 'cancelled', '已取消'

    class PayType(models.IntegerChoices):
        ONLINE = 1, '在线支付'
        COD = 2, '到付'

    class PayStatus(models.IntegerChoices):
        UNPAID = 0, '未支付'
        PAID = 1, '已支付'
        REFUNDING = 2, '退款中'
        REFUNDED = 3, '已退款'

    order_no = models.CharField('订单号', max_length=32, unique=True)
    tracking_id = models.CharField('运单号', max_length=20, unique=True, null=True, blank=True)

    # 寄件人
    sender_name = models.CharField('寄件人姓名', max_length=50)
    sender_phone = models.CharField('寄件人电话', max_length=20)
    sender_province = models.CharField('寄件省份', max_length=50)
    sender_city = models.CharField('寄件城市', max_length=50)
    sender_district = models.CharField('寄件区县', max_length=50)
    sender_address = models.CharField('寄件详细地址', max_length=200)

    # 收件人
    receiver_name = models.CharField('收件人姓名', max_length=50)
    receiver_phone = models.CharField('收件人电话', max_length=20)
    receiver_province = models.CharField('收件省份', max_length=50)
    receiver_city = models.CharField('收件城市', max_length=50)
    receiver_district = models.CharField('收件区县', max_length=50)
    receiver_address = models.CharField('收件详细地址', max_length=200)

    # 包裹信息
    weight = models.DecimalField('重量(kg)', max_digits=10, decimal_places=2)
    volume = models.DecimalField('体积(m³)', max_digits=10, decimal_places=2, null=True, blank=True)
    length = models.DecimalField('长度(cm)', max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField('宽度(cm)', max_digits=10, decimal_places=2, null=True, blank=True)
    height = models.DecimalField('高度(cm)', max_digits=10, decimal_places=2, null=True, blank=True)
    goods_type = models.CharField('物品类别', max_length=50)
    goods_desc = models.TextField('物品描述', blank=True)
    is_insured = models.BooleanField('是否保价', default=False)
    insured_amount = models.DecimalField('保价金额', max_digits=10, decimal_places=2, null=True, blank=True)

    # 费用
    freight_fee = models.DecimalField('运费', max_digits=10, decimal_places=2, default=0)
    insurance_fee = models.DecimalField('保价费', max_digits=10, decimal_places=2, default=0)
    packaging_fee = models.DecimalField('包装费', max_digits=10, decimal_places=2, default=0)
    total_fee = models.DecimalField('总费用', max_digits=10, decimal_places=2, default=0)
    pay_type = models.IntegerField('付款方式', choices=PayType.choices, default=PayType.ONLINE)
    pay_status = models.IntegerField('支付状态', choices=PayStatus.choices, default=PayStatus.UNPAID)
    pay_time = models.DateTimeField('支付时间', null=True, blank=True)

    # 服务选项
    express_company = models.CharField('快递公司编码', max_length=20)
    pick_up_time = models.DateTimeField('预约取件时间', null=True, blank=True)
    packaging_method = models.CharField('包装方式', max_length=50, blank=True)
    is_collect_on_delivery = models.BooleanField('是否代收货款', default=False)
    cod_amount = models.DecimalField('代收金额', max_digits=10, decimal_places=2, null=True, blank=True)

    # 关联与状态
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    courier = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery_tasks', verbose_name='分配快递员')
    branch = models.ForeignKey('stations.Branch', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属网点')
    order_status = models.CharField('订单状态', max_length=20, choices=OrderStatus.choices, default=OrderStatus.WAITING_PICKUP)
    remark = models.TextField('备注', blank=True)

    # 签收信息
    sign_image = models.URLField('签收凭证图片', blank=True)
    sign_photo = models.URLField('包裹拍照凭证', blank=True)
    sign_time = models.DateTimeField('签收时间', null=True, blank=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单管理'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_no']),
            models.Index(fields=['tracking_id']),
            models.Index(fields=['order_status']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'订单 {self.order_no} - {self.get_order_status_display()}'


class PaymentRecord(models.Model):
    """支付记录"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name='订单')
    pay_no = models.CharField('支付流水号', max_length=64, unique=True)
    pay_type = models.CharField('支付方式', max_length=20, choices=[('wxpay', '微信支付'), ('alipay', '支付宝'), ('balance', '预充值')])
    amount = models.DecimalField('支付金额', max_digits=10, decimal_places=2)
    pay_status = models.CharField('支付状态', max_length=20, choices=[('pending', '处理中'), ('success', '成功'), ('failed', '失败'), ('refunded', '已退款')])
    pay_time = models.DateTimeField('支付时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录管理'

    def __str__(self):
        return f'{self.pay_no} - ¥{self.amount}'
