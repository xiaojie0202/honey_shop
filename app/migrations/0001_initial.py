# Generated by Django 2.1.5 on 2019-04-10 03:01

import DjangoUeditor.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('desc', models.CharField(max_length=256, verbose_name='商品简介')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('unite', models.CharField(max_length=20, verbose_name='商品单位')),
                ('image', models.ImageField(upload_to='goods', verbose_name='商品图片')),
                ('variety', models.CharField(max_length=20, verbose_name='品种')),
                ('manufacturing_season', models.CharField(max_length=20, verbose_name='季节')),
                ('address', models.CharField(max_length=64, verbose_name='产地')),
                ('stock', models.IntegerField(default=1, verbose_name='商品库存')),
                ('sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('status', models.SmallIntegerField(choices=[(0, '下线'), (1, '上线')], default=1, verbose_name='商品状态')),
                ('detail', DjangoUeditor.models.UEditorField(verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品信息',
                'verbose_name_plural': '商品信息',
                'db_table': 'goods',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='商品数目')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('comment', models.CharField(default='', max_length=256, verbose_name='评论')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
                'db_table': 'df_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('order_id', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='订单id')),
                ('pay_method', models.SmallIntegerField(choices=[(1, '货到付款'), (2, '微信支付'), (3, '支付宝'), (4, '银联支付')], default=3, verbose_name='支付方式')),
                ('total_count', models.IntegerField(default=1, verbose_name='商品数量')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品总价')),
                ('transit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='订单运费')),
                ('order_status', models.SmallIntegerField(choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], default=1, verbose_name='订单状态')),
                ('trade_no', models.CharField(default='', max_length=128, verbose_name='支付编号')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
                'db_table': 'df_order_info',
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.CharField(max_length=20, verbose_name='收件人')),
                ('addr', models.CharField(max_length=256, verbose_name='收件地址')),
                ('zip_code', models.CharField(max_length=6, null=True, verbose_name='邮政编码')),
                ('phone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否默认')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属账户')),
            ],
            options={
                'verbose_name': '地址',
                'verbose_name_plural': '地址',
                'db_table': 'user_address',
            },
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='addr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserAddress', verbose_name='地址'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.OrderInfo', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Goods', verbose_name='商品'),
        ),
    ]
