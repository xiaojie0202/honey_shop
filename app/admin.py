from django.contrib import admin
from app import models


# Register your models here.


@admin.register(models.Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'unite']



admin.site.site_header = '爱蜜蜂'
admin.site.site_title = '爱蜜蜂'
