from django.contrib import admin
from payments.models import orderPayment, additionalPricePayment
from django.utils.html import format_html

# Register your models here.

class orderPaymentAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="80" height="80" style="border-radius:20%;">'.format(object.user.avatar.url))
    thumbnail.short_description = 'Avatar'
    list_display = ('thumbnail', 'payment_id', 'order_number', 'status')
    list_display_links=( 'thumbnail','payment_id',)
    list_filter = ('payment_id', 'order_number','user')
    search_fields = ('payment_id', 'order_number', 'user')
admin.site.register(orderPayment,orderPaymentAdmin)

class additionalPricePaymentAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="80" height="80" style="border-radius:20%;">'.format(object.user.avatar.url))
    thumbnail.short_description = 'Avatar'
    list_display = ('thumbnail', 'payment_id', 'order', 'status')
    list_display_links=( 'thumbnail','payment_id',)
    list_filter = ('payment_id', 'order', 'user')
    search_fields = ('payment_id', 'order', 'user')
admin.site.register(additionalPricePayment,additionalPricePaymentAdmin)