from django.forms import ModelForm
from .models import User, Order
from django import forms
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm


class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'phone', 'country',  'user_address']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email',  'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email']




class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order_status'].required = False 
        self.fields['order_status'].initial = 'active'  # Set a default value for order_status
        self.fields['order_date'].initial = timezone.now  # Set today's date as the default value, you can replace it with your desired default date
    
    class Meta:
        model = Order
        exclude = ['user']  # Exclude the 'user' field from the form
        fields = '__all__'  # Include all fields from the model
        # exclude = ['price']  # Exclude the 'price' field from the form, as it will be calculated in the view