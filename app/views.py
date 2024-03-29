from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger
from app import models
from app.utils import CustomPaginator
import json
from uuid import uuid4
from django.utils.functional import SimpleLazyObject


# Create your views here.

# 登陆
def acc_login(request):
    if request.method == 'GET':
        return render(request, 'app/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            return render(request, 'app/login.html', {'erro': "用户名或密码错误"})


# 注册
def acc_register(request):
    if request.method == 'GET':
        return render(request, 'app/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_namr = request.POST.get('firstname')

        a = models.User.objects.filter(username=username).first()

        if password1 == password2:
            if a:
                return JsonResponse({'status': False, 'erro': '当前用户名已经存在!'})
            user = models.User.objects.create_user(username=username, password=password2, first_name=first_namr,
                                                   email='xxzzyy@qq.com')
            return JsonResponse({'status': True})


# 注销
def acc_logout(request):
    """注销视图函数"""
    logout(request)
    return redirect('/login')


# 主页
def index(request):
    return render(request, 'app/index.html')


# 商城
def shop(request):
    """
    购物车数量
    所有品种， 季节， 地区
    所有商品
    :param request:
    :return:
    """
    goods_obj = models.Goods.objects.filter(status=1)
    # 品种， 季节， 地区
    temp_dict = {
        'variety': list(set([i[0] for i in goods_obj.values_list('variety')])),
        'manufacturing_season': list(set([i[0] for i in goods_obj.values_list('manufacturing_season')])),
        'address': list(set([i[0] for i in goods_obj.values_list('address')])),
    }

    # 当前用户的购物车数量

    # 过滤相关
    filter_dict = {}

    current_page = request.GET.get('page', 1)
    search = request.GET.get('search')
    variety = request.GET.get('variety')
    manufacturing_season = request.GET.get('manufacturing_season')
    address = request.GET.get('address')

    if search:
        goods_obj = goods_obj.filter(name__icontains=search)
        filter_dict['search'] = search
    if variety:
        goods_obj = goods_obj.filter(variety=variety)
        filter_dict['variety'] = variety
    if manufacturing_season:
        goods_obj = goods_obj.filter(manufacturing_season=manufacturing_season)
        filter_dict['manufacturing_season'] = manufacturing_season
    if address:
        goods_obj = goods_obj.filter(address=address)
        filter_dict['address'] = address

    if current_page == 'all':
        paginator = CustomPaginator(1, 10, goods_obj, goods_obj.count())
    else:
        paginator = CustomPaginator(current_page, 10, goods_obj, 60)

    try:
        data_list = paginator.page(current_page)  # 分页
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    context = {
        'goods_obj': data_list,
        'filter_dict': filter_dict,
    }
    context.update(temp_dict)

    return render(request, 'app/shop_list.html', context)


# 商品详情页面
@login_required
def good_dearil(request, goodsid):
    good_obj = models.Goods.objects.filter(pk=goodsid).first()

    #  当前用户的购物车数量


    cart_count = models.ShopCart.objects.filter(user=request.user).count()

    return render(request, 'app/detail.html', {'good_obj': good_obj, 'cart_count': cart_count})


# 购物车页
@login_required
def shop_cart(request):
    shop_cart_obj = models.ShopCart.objects.filter(user=request.user)

    # 总价
    price = 0
    for cart in shop_cart_obj:
        price += cart.good.price * cart.good_count
    # 商品数量
    return render(request, 'app/shop_cart.html', {'shop_cart_obj': shop_cart_obj, 'price': price})


# 结算页面
@login_required
def place_order(request):
    if request.method == 'GET':
        # 获取用户传递过来的商品

        order = request.GET.get('order')
        # order = 1-3,3-3 商品ID-商品数量
        data = []
        dd2 = []
        all_price = 0
        for a in order.split(','):
            if a:
                good_id, good_count, *_ = a.split('-')
                good = models.Goods.objects.filter(pk=good_id).first()
                all_price += good.price * int(good_count)
                data.append({'good': good, 'count': int(good_count)})
                dd2.append({'good_id': good.id, 'good_count': int(good_count)})
        # 用户地址
        addrs = models.UserAddress.objects.filter(user=request.user)
        # 计算总金额额
        context = {
            'good_list': data, 'count': len(data), 'all_price': all_price, 'all_price2': all_price + 10,
            'addrs': addrs,
            'dd2': dd2
        }
        return render(request, 'app/place_order.html', context)
    elif request.method == 'POST':
        data = request.POST.get('data')
        data = json.loads(data)
        good_obj_list = []  # 存放所有商品对象
        sum_price = 0  # 总价

        # {'goods': [{'good_id': 1, 'good_count': 3}, {'good_id': 3, 'good_count': 3}], 'addr_id': '1', 'pay_type': '1'}
        for d in data['goods']:
            a = models.Goods.objects.filter(pk=d['good_id']).first()
            b = models.ShopCart.objects.filter(user=request.user, good_id=d['good_id'])
            if b:
                b.delete()
            if a:
                good_obj_list.append([a, int(d['good_count'])])
            sum_price += a.price * int(d['good_count'])

        # 生成订单
        order_obj = models.OrderInfo.objects.create(
            order_id=str(uuid4()),
            user=request.user,
            addr_id=data['addr_id'],
            pay_method=int(data['pay_type']),
            total_count=len(good_obj_list),
            total_price=sum_price,
            transit_price=10,

        )
        # 生成所有商品
        for good_obj, count in good_obj_list:
            models.OrderGoods.objects.create(
                order=order_obj,
                sku=good_obj,
                count=count,
                price=good_obj.price * count,
            )

        print(data)
        return JsonResponse({'status': True})


# 用户信息页面
@login_required
def user_center_info(request):
    return render(request, 'app/user_center_info.html')


# 用户订单页面
@login_required
def user_center_order(request):
    # 查询用户所有订单
    order_obj = models.OrderInfo.objects.filter(user=request.user).order_by('create_datetime')
    context = {
        'order_obj': order_obj
    }
    return render(request, 'app/user_center_order.html', context)


# 用户地址管理页面
@login_required
def user_center_site(request):
    if request.method == 'GET':
        addr_obj = models.UserAddress.objects.filter(user=request.user)

        return render(request, 'app/user_center_site.html', {'addr_obj': addr_obj})
    elif request.method == 'POST':
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        if all([receiver, addr, zip_code, phone]):
            a = models.UserAddress.objects.create(receiver=receiver, addr=addr, zip_code=zip_code, phone=phone,
                                                  user=request.user)
        return redirect('/user_center_site')


# 设置用户默认地址
def set_default_addr(request):
    addr_id = request.POST.get('addrID')
    addr_obj = models.UserAddress.objects.filter(user=request.user)
    addr_obj.update(is_default=False)
    addr_obj.filter(pk=addr_id).update(is_default=True)
    return JsonResponse({'status': True})


# 添加商品到购物车
@login_required
def add_cart(request):
    user = request.user
    good_id = request.POST.get('GoodID')
    good_count = request.POST.get('GoodCount')
    if good_id and good_count:
        car_obj = models.ShopCart.objects.filter(user=user, good=good_id).first()
        if car_obj:
            car_obj.good_count = car_obj.good_count + int(good_count)
            car_obj.save()
            return JsonResponse({'status': True, 'new': False})
        else:
            models.ShopCart.objects.create(user=user, good_id=good_id, good_count=good_count)
            return JsonResponse({'status': True, 'new': True})
    else:
        return JsonResponse({'status': False})


@login_required
def remove_cart(request):
    user = request.user
    car_id = request.POST.get('carID')
    car_obj = models.ShopCart.objects.filter(user=user, pk=car_id).first()
    if car_obj:
        car_obj.delete()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False})


# 支付
@login_required
def pay(request):
    order_id = request.POST.get('orderID')
    a = models.OrderInfo.objects.filter(order_id=order_id).first()
    a.order_status = 3
    a.trade_no = str(uuid4())
    a.save()
    return JsonResponse({'status': True})


# 确认收货
@login_required
def receiving(request):
    order_id = request.POST.get('orderID')
    a = models.OrderInfo.objects.filter(order_id=order_id).first()
    a.order_status = 4
    a.save()
    return JsonResponse({'status': True})
