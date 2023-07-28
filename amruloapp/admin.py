#Admin
#=> admin (admin)
#=> amrulo (password)
#=> amrulo@gmail.com (email)


from django.contrib import admin
from .models import User, Order

#Registered here

admin.site.register(User)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'order_type', 'salesman', 'production', 'price', 'order_date')
    list_filter = ('order_type', 'production', 'price', 'order_date')
    search_fields = ('id', 'customer_name', 'salesman', 'order_date')

    # def formatted_price(self, obj):
    #     currency_indicator = "$" if obj.currency == 'USD' else "Rs."
    #     return f"{currency_indicator}{obj.price:.2f}"

    # formatted_price.admin_order_field = 'price'
    # formatted_price.short_description = 'Price'

admin.site.register(Order, OrderAdmin)