from django.contrib import admin
from products.models import (
    OriginalData,DesignPrinting,ProductType,ProductSubType,
    ProductMaterial,UnitOfMeasurement,DeliveryTiming,
    Product12HrsPrice,Product6HrsPrice,Product2HrsPrice,Product
    )
# Register your models here.

class OriginalDataAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links=( 'name',)
    search_fields = ('name',)
admin.site.register(OriginalData,OriginalDataAdmin)
class DesignPrintingAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links=( 'name',)
    search_fields = ('name',)
admin.site.register(DesignPrinting,OriginalDataAdmin)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links=( 'name',)
    search_fields = ('name',)
admin.site.register(ProductType,OriginalDataAdmin)
class ProductSubTypeAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links=('name',)
    search_fields = ('name',)
admin.site.register(ProductSubType,ProductSubTypeAdmin)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('id','product_sub_type','name',)
    list_display_links=('product_sub_type','name',)
    search_fields = ('name',)
admin.site.register(ProductMaterial,ProductMaterialAdmin)
class UnitOfMeasurementAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links=('name',)
    search_fields = ('name',)
admin.site.register(UnitOfMeasurement,UnitOfMeasurementAdmin)
class DeliveryTimingAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links=( 'name',)
    search_fields = ('name',)
admin.site.register(DeliveryTiming,DeliveryTimingAdmin)
class Product12HrsPriceAdmin(admin.ModelAdmin):
    list_display = ('id','product_sub_type','delivery_timing','price',)
    list_display_links=('product_sub_type','delivery_timing',)
    list_filter = ('delivery_timing',)
    search_fields = ('product_sub_type','delivery_timing',)
admin.site.register(Product12HrsPrice,Product12HrsPriceAdmin)
class Product6HrsPriceAdmin(admin.ModelAdmin):
    list_display = ('id','product_sub_type','delivery_timing','price',)
    list_display_links=('product_sub_type','delivery_timing',)
    list_filter = ('delivery_timing',)
    search_fields = ('product_sub_type','delivery_timing',)
admin.site.register(Product6HrsPrice,Product6HrsPriceAdmin)
class Product2HrsPriceAdmin(admin.ModelAdmin):
    list_display = ('id','product_sub_type','delivery_timing','price',)
    list_display_links=('product_sub_type','delivery_timing',)
    list_filter = ('delivery_timing',)
    search_fields = ('product_sub_type','delivery_timing',)
admin.site.register(Product2HrsPrice,Product2HrsPriceAdmin)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_sub_type','product_12hrs_price','product_6hrs_price','product_2hrs_price',)
    list_display_links=('product_sub_type',)
    list_filter = ('product_sub_type',)
    search_fields = ('product_sub_type',)
admin.site.register(Product,ProductAdmin)