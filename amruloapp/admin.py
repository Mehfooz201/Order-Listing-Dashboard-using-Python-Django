#Admin
#=> admin (admin)
#=> amrulo (password)
#=> amrulo@gmail.com (email)


from django.contrib import admin
from .models import User

#Registered here

admin.site.register(User)