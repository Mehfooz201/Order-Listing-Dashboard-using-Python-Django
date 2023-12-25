
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django import forms
from cdlapp.forms import MyUserCreationForm, OrderForm, MyUserUpdateForm
from .models import User, Order, OrderGallery, CompanyInformation, FrameworkAgreement, FrameworkInformation
from django.utils.html import format_html
import os
from django.conf import settings


#Registered here

"""class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password','name','email','username','phone']
"""
class UserAdminModel(admin.ModelAdmin):
    form = MyUserCreationForm
    change_form = MyUserUpdateForm
    def thumbnail(self, object):
        return format_html('<img src="{}" width="80" height="80" style="border-radius:20%;">'.format(object.avatar.url))
    thumbnail.short_description = 'Avatar'
    readonly_fields=('last_login','date_joined','password')
    list_display = ('thumbnail','email', 'name',  'company_information','is_active')
    list_display_links=( 'thumbnail','email',)
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ('email', 'company_information','name',)
    search_fields = ('name', 'email', 'company_information',)

    class Media:
        js = ('cdlapp/js/user_admin_form.js', )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created i.e. it's an edit
            return ['last_login', 'date_joined', 'password']
        else:
            return ['last_login', 'date_joined']

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # This is the case when obj is being created
            return self.form
        else:  # This is the case when obj already exists i.e. it's being changed
            return self.change_form

    def get_fieldsets(self, request, obj=None):
        if obj:
            return [(
                None, {
                    'fields': (
                        'avatar', 'email', 'username', 'first_name', 'last_name', 'name', 'approval_status', 'company_information', 'country', 'user_address',
                        'is_admin', 'is_staff', 'is_active', 'is_superadmin','groups', 'user_permissions',
                        ),
                    }
                    )]
        return [(None, {'fields': ('email', 'username', 'name','phone', 'password1', 'password2', 'user_password')})]

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

class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order
        fields = '__all__'
        # exclude = ['']
    def thumbnail(self, object):
        return format_html('<img src="{}" width="80" height="80" style="border-radius:20%;">'.format(object.user.avatar.url))
    thumbnail.short_description = 'Avatar'
    list_display = ('thumbnail','customer_name', 'order_number',  'order_status', 'order_type', 'price', 'order_date', 'is_ordered')
    list_display_links=( 'thumbnail','order_number','customer_name',)
    list_filter = ('order_status', 'order_date')
    search_fields = ('order_number', 'customer_name', 'order_status', 'order_date')

    # form = OrderForm
    class Media:
        js = ('cdlapp/js/order_admin_form.js', )
               
    # def save_related(self, request, form, formsets, change):
    #     super().save_related(request, form, formsets, change)
    #     form.save_photos(form.instance)

class OrderGalleryAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        try:
            if (str(object.image.url).split('.')[-1]=="bmp" or
                str(object.image.url).split('.')[-1]=="jpg" or
                str(object.image.url).split('.')[-1]=="jpeg" or
                str(object.image.url).split('.')[-1]=="png" or
                str(object.image.url).split('.')[-1]=="gif" or
                str(object.image.url).split('.')[-1]=="BMP" or
                str(object.image.url).split('.')[-1]=="JPG" or
                str(object.image.url).split('.')[-1]=="JPEG" or
                str(object.image.url).split('.')[-1]=="PNG" or
                str(object.image.url).split('.')[-1]=="GIF"):
                return format_html('<img src="{}" width="80" style="border-radius:10%;border:1px solid #000">'.format(object.image.url))
            else:
                pdf_icon = os.path.join(settings.STATIC_URL,"cdlapp/assets/images/pdf-file.png")
                stl_icon = os.path.join(settings.STATIC_URL,"cdlapp/assets/images/stl-file.png")
                dcm_icon = os.path.join(settings.STATIC_URL,"cdlapp/assets/images/dcm-file.png")
                html_icon = os.path.join(settings.STATIC_URL,"cdlapp/assets/images/html-file.png")

                if (str(object.image.url).split('.')[-1]=="pdf" or str(object.image.url).split('.')[-1]=="PDF"):
                    return format_html('<img src="{}" width="80" style="border-radius:10%;border:1px solid #000">'.format(pdf_icon))
                elif (str(object.image.url).split('.')[-1]=="stl" or str(object.image.url).split('.')[-1]=="STL"):
                    return format_html('<img src="{}" width="80" style="border-radius:10%;border:1px solid #000">'.format(stl_icon))
                elif (str(object.image.url).split('.')[-1]=="dcm" or str(object.image.url).split('.')[-1]=="DCM"):
                    return format_html('<img src="{}" width="80" style="border-radius:10%;border:1px solid #000">'.format(dcm_icon))
                elif (str(object.image.url).split('.')[-1]=="html" or str(object.image.url).split('.')[-1]=="HTML"):
                    return format_html('<img src="{}" width="80" style="border-radius:10%;border:1px solid #000">'.format(html_icon))
        except:
            pass

    thumbnail.short_description = 'File Uploaded'
    list_display = ("thumbnail", "order", "image",)
    list_display_links = ("thumbnail", "order", "image",)
    list_filter = ('order',)
    search_fields = ('order', 'title',)
    filter_horizontal=()
    fieldsets=()

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderGallery, OrderGalleryAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_phone')
admin.site.register(CompanyInformation, CompanyAdmin)

