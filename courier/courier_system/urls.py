from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    # 订单管理
    path('orders/', include('orders.urls')),
    # 物流查询
    path('tracking/', include('tracking.urls')),
    # 地址簿
    path('addresses/', include('users.urls')),
    # 快递员端
    path('courier/', include('couriers.urls')),
    # 驿站端
    path('station/', include('stations.urls')),
    # 管理看板
    path('admin-dashboard/', include('dashboard.urls')),

    # Django Admin
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else '')
