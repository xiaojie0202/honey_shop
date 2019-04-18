# 爱蜂蜜电商网站

## 开发环境
    python3.7
## 依赖环境
    pip install Django==2.1.5
    pip install PyMySQL==0.9.3
    
```
# 安装 DjangoUeditor3（百度的富文本编辑器）
下载
    https://github.com/twz915/DjangoUeditor3
    (已经下载到项目根目录DjangoUeditor3-master.zip)
安装
    pip install DjangoUeditor3-master.zip

```
## 配置数据库

```
# settings.py

找到配置信息

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库名字',
        'USER': '数据库用户名',
        'PASSWORD': '数据库密码',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

```
>- 迁移操作
    python manage.py makemigrations
    python manage.py migrate
    
## 运行
    python manage.py runserver



## 项目截图
![](https://github.com/xiaojie0202/honey_shop/blob/master/static/media/%E6%88%AA%E5%9B%BE1.png)
![](https://github.com/xiaojie0202/honey_shop/blob/master/static/media/%E6%88%AA%E5%9B%BE2.png)
![](https://github.com/xiaojie0202/honey_shop/blob/master/static/media/%E6%88%AA%E5%9B%BE3.png)
![](https://github.com/xiaojie0202/honey_shop/blob/master/static/media/%E6%88%AA%E5%9B%BE4.png)
![](https://github.com/xiaojie0202/honey_shop/blob/master/static/media/%E6%88%AA%E5%9B%BE5.png)
