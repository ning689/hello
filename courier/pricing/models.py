from django.db import models


class FreightTemplate(models.Model):
    """运费模板"""
    MODE_CHOICES = [
        ('weight', '按重量计费'),
        ('volume', '按体积计费'),
        ('piece', '按件计费'),
    ]
    name = models.CharField('模板名称', max_length=100)
    express_company = models.CharField('快递公司编码', max_length=20)
    mode = models.CharField('计费模式', max_length=10, choices=MODE_CHOICES, default='weight')
    first_weight = models.DecimalField('首重(kg)', max_digits=10, decimal_places=2, default=1.0)
    first_price = models.DecimalField('首重价格', max_digits=10, decimal_places=2)
    additional_weight = models.DecimalField('续重(kg)', max_digits=10, decimal_places=2, default=1.0)
    additional_price = models.DecimalField('续重价格', max_digits=10, decimal_places=2)
    free_shipping_threshold = models.DecimalField('包邮门槛(元)', max_digits=10, decimal_places=2, null=True, blank=True)
    remote_area_surcharge = models.DecimalField('偏远地区附加费', max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField('启用', default=True)
    version = models.CharField('版本号', max_length=20, blank=True)
    effective_date = models.DateField('生效日期')
    expire_date = models.DateField('失效日期', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '运费模板'
        verbose_name_plural = '运费模板管理'

    def __str__(self):
        return f'{self.name} ({self.express_company})'


class FreightRule(models.Model):
    """运费规则（按地区维度）"""
    template = models.ForeignKey(FreightTemplate, on_delete=models.CASCADE, related_name='rules', verbose_name='模板')
    province = models.CharField('省份', max_length=50)
    city = models.CharField('城市', max_length=50, blank=True)
    district = models.CharField('区县', max_length=50, blank=True)
    first_price_override = models.DecimalField('首重价格(覆盖)', max_digits=10, decimal_places=2, null=True, blank=True)
    additional_price_override = models.DecimalField('续重价格(覆盖)', max_digits=10, decimal_places=2, null=True, blank=True)
    surcharge = models.DecimalField('附加费', max_digits=10, decimal_places=2, default=0)
    is_remote_area = models.BooleanField('偏远地区', default=False)

    class Meta:
        verbose_name = '运费规则'
        verbose_name_plural = '运费规则管理'

    def __str__(self):
        return f'{self.province}-{self.city} ({self.template.name})'


class InsuranceRate(models.Model):
    """保价费率配置"""
    min_amount = models.DecimalField('最低保价金额', max_digits=10, decimal_places=2)
    max_amount = models.DecimalField('最高保价金额', max_digits=10, decimal_places=2)
    rate = models.DecimalField('费率(%)', max_digits=5, decimal_places=2)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '保价费率'
        verbose_name_plural = '保价费率配置'

    def __str__(self):
        return f'¥{self.min_amount}-¥{self.max_amount}: {self.rate}%'
