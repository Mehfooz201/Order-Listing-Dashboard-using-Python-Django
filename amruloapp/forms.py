from django.forms import ModelForm
from .models import User, Order
from django import forms
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm


#Staff User
class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'phone', 'password1', 'password2']

   

#User Form
class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'phone', 'country',  'user_address']


class MyUserCreationForm(forms.ModelForm):
    
    user_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["user_password","confirm_password"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email']


class RemakeRequestForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['remake_notes', 'num_crowns', 'num_brackets']



class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order_status'].required = False 
        self.fields['order_status'].initial = 'review'  # Set a default value for order_status
        self.fields['order_date'].initial = timezone.now  # Set today's date as the default value, you can replace it with your desired default date
    
    class Meta:
        model = Order
        exclude = ['user', 'remake_notes', 'num_crowns', 'num_brackets', 'remake_price']  # Exclude the 'user' field from the form
        fields = '__all__'  # Include all fields from the model
        # exclude = ['price']  # Exclude the 'price' field from the form, as it will be calculated in the view






class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_('Email'), max_length=250, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))



class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
