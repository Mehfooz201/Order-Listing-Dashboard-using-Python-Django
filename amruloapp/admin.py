#Admin
#=> admin (lab)
#=> project12 (password)
#=> amrulo@gmail.com (email)


from django.contrib import admin
from .models import User, Order, StaffUser

#Registered here

admin.site.register(User)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'order_status', 'order_type', 'salesman', 'price', 'order_date')
    list_filter = ('order_number', 'customer_name', 'order_status', 'order_type',  'price', 'order_date')
    search_fields = ('order_number', 'customer_name', 'order_status', 'salesman', 'order_date')

admin.site.register(Order, OrderAdmin)

class StaffUserAdmin(admin.ModelAdmin):
    list_display = ('approval_status',)
admin.site.register(StaffUser, StaffUserAdmin)