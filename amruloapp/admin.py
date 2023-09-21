#Admin
#=> admin (lab)
#=> project12 (password)
#=> amrulo@gmail.com (email)


from django.contrib import admin
from django import forms
from .models import User, Order, CompanyInformation, FrameworkAgreement, FrameworkInformation
from django.utils.html import format_html

#Registered here

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','email','password','username','phone','groups']

class UserAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="80" height="80" style="border-radius:20%;">'.format(object.avatar.url))
    thumbnail.short_description = 'Avatar'
    list_display = ('thumbnail','email', 'name',  'company_information',)
    list_display_links=( 'thumbnail','email',)
    list_filter = ('email', 'company_information','name',)
    search_fields = ('name', 'email', 'company_information',)
    form = CustomUserForm
admin.site.register(User,UserAdmin)



admin.site.register(FrameworkAgreement)
admin.site.register(FrameworkInformation)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class OrderAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="80" height="80" style="border-radius:20%;">'.format(object.user.avatar.url))
    thumbnail.short_description = 'Avatar'
    list_display = ('thumbnail','customer_name', 'order_number',  'order_status', 'order_type', 'salesman', 'price', 'order_date')
    list_display_links=( 'thumbnail','order_number','customer_name',)
    list_filter = ('customer_name', 'order_status', 'order_date')
    search_fields = ('order_number', 'customer_name', 'order_status', 'order_date')
    form = OrderForm
    class Media:
        js = ('amruloapp/js/order_admin_form.js', )

admin.site.register(Order, OrderAdmin)



class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_phone')
admin.site.register(CompanyInformation, CompanyAdmin)

