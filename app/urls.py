"""honey_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),  # 主页
    path('shop', views.shop, name='shop'), # 商城
    path('detail/<int:goodsid>', views.good_dearil, name='goodderail'),  # 商品详情
    path('cart', views.shop_cart, name='cart'),  # 购物车页面
    path('place_order', views.place_order, name='place_order'),  # 提交订单页面
    path('user_center_info', views.user_center_info),  # 用户信息页面
    path('user_center_order', views.user_center_order),  # 也用户订单
    path('user_center_site', views.user_center_site),  # 用户地址
    path('set_default_addr', views.set_default_addr),  # 用户地址
    path('login', views.acc_login),  # 登陆
    path('register', views.acc_register),  # 注册
    path('logout', views.acc_logout), #注销
    path('add_cart', views.add_cart), # 添加购物车
    path('remove_cart', views.remove_cart), # 删除购物车商品
    path('pay', views.pay), # 删除购物车商品
    path('receiving', views.receiving), # 删除购物车商品

]
