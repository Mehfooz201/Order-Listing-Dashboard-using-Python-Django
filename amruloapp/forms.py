from django.forms import ModelForm
from .models import User, Order
from django import forms
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email']


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order_date'].initial = timezone.now  # Set today's date as the default value, you can replace it with your desired default date
    
    class Meta:
        model = Order
        fields = '__all__'  # Include all fields from the model
        # exclude = ['price']  # Exclude the 'price' field from the form, as it will be calculated in the view