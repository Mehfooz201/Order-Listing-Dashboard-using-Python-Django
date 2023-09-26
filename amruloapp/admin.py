#Admin
#=> admin (lab)
#=> project12 (password)
#=> amrulo@gmail.com (email)

from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django import forms
from amruloapp.forms import MyUserCreationForm
from .models import User, Order, CompanyInformation, FrameworkAgreement, FrameworkInformation
from django.utils.html import format_html
from django.contrib.auth.models import Group

#Registered here

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password','name','email','username','phone']

class UserAdminModel(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="80" height="80" style="border-radius:20%;">'.format(object.avatar.url))
    thumbnail.short_description = 'Avatar'
    readonly_fields=('last_login','date_joined','password')
    list_display = ('thumbnail','email', 'name',  'company_information','is_active',)
    list_display_links=( 'thumbnail','email',)
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ('email', 'company_information','name',)
    search_fields = ('name', 'email', 'company_information',)

    class Media:
        js = ('amruloapp/js/user_admin_form.js', )

    def get_fieldsets(self, request, obj=None):
        if obj:
            return [(
                None, {
                    'fields': (
                        'password', 'avatar', 'email', 'username', 'first_name', 'last_name', 'name', 'approval_status', 'company_information', 'country', 'user_address',
                        'is_admin', 'is_staff', 'is_active', 'is_superadmin','groups', 'user_permissions',
                        ),
                    }
                    )]
        return [(None, {'fields': ('email', 'username', 'name','phone','user_password','confirm_password',)})]

    #def get_form(self, request, obj=None, **kwargs):
    #    if obj:
    #        defaults = {'exclude': ('user_password','confirm_password',)}
    #    else:
    #        defaults = {}
    #    defaults.update(kwargs)
    #    return super(UserAdminModel, self).get_form(request, obj, **defaults)
        
    def has_add_permission(self, request):
        return request.user.is_superadmin

    def has_change_permission(self, request, obj=None):
        return request.user.is_superadmin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superadmin
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superadmin
        

admin.site.register(User, UserAdminModel)


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

