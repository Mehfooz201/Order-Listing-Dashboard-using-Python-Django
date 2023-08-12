#Admin
#=> admin (lab)
#=> project12 (password)
#=> amrulo@gmail.com (email)


from django.contrib import admin
from .models import User, Order, CompanyInformation, FrameworkAgreement

#Registered here

admin.site.register(User)

admin.site.register(FrameworkAgreement)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'order_status', 'order_type', 'salesman', 'price', 'order_date')
    list_filter = ('order_number', 'customer_name', 'order_status', 'order_type',  'price', 'order_date')
    search_fields = ('order_number', 'customer_name', 'order_status', 'salesman', 'order_date')

admin.site.register(Order, OrderAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_phone')

admin.site.register(CompanyInformation, CompanyAdmin)

