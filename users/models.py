from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """扩展用户模型 - 支持四种角色"""
    ROLE_CHOICES = [
        ('user', 'C端用户'),
        ('courier', '快递员'),
        ('station_admin', '驿站管理员'),
        ('admin', '后台管理员'),
    ]
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='user')
    phone = models.CharField('手机号', max_length=20, unique=True)
    avatar = models.URLField('头像', blank=True)
    branch = models.ForeignKey('stations.Branch', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属网点')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return f'{self.get_role_display()}: {self.username or self.phone}'


class Address(models.Model):
    """地址簿"""
    LABEL_CHOICES = [
        ('home', '家'),
        ('company', '公司'),
        ('school', '学校'),
        ('other', '其他'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    label = models.CharField('标签', max_length=10, choices=LABEL_CHOICES, default='other')
    name = models.CharField('联系人', max_length=50)
    phone = models.CharField('联系电话', max_length=20)
    province = models.CharField('省份', max_length=50)
    city = models.CharField('城市', max_length=50)
    district = models.CharField('区县', max_length=50)
    detail = models.CharField('详细地址', max_length=200)
    is_default = models.BooleanField('默认地址', default=False)
    last_used = models.DateTimeField('最近使用', auto_now=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '地址簿'
        verbose_name_plural = '地址簿管理'
        ordering = ['-is_default', '-last_used']

    def __str__(self):
        return f'{self.label}: {self.province}{self.city}{self.district}{self.detail}'
