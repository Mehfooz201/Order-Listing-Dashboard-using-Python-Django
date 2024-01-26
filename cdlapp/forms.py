from django.forms import ModelForm
from .models import User, Order, OrderGallery
from django import forms
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm


#Staff User
class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'phone', 'password1', 'password2', 'user_password']
        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get('password1')
            user_password = cleaned_data.get('user_password')
            if password1 != user_password:
                raise forms.ValidationError('Passwords do not match')
            return cleaned_data

   

#User Form
class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'phone', 'country',  'user_address']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'phone', 'password1', 'password2', 'user_password']
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        user_password = cleaned_data.get('user_password')
        if password1 != user_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'email', 'username', 'first_name', 'last_name', 'name', 'approval_status', 'company_information', 'country', 'user_address',
                        'is_admin', 'is_staff', 'is_active', 'is_superadmin','groups', 'user_permissions']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'user_password']


class RemakeRequestForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['remake_notes', 'num_crowns', 'num_brackets', 'upper_arch', 'lower_arch']



class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order_status'].required = False 
        self.fields['order_status'].initial = 'review'  # Set a default value for order_status
        self.fields['order_date'].initial = timezone.now  # Set today's date as the default value, you can replace it with your desired default date

    class Meta:
        model = Order
        exclude = ['user', 'remake_notes', 'num_crowns', 'num_brackets', 'remake_price', 'upper_arch', 'lower_arch', 'commentOrRemarks']  # Exclude the 'user' field from the form
        fields = '__all__'  # Include all fields from the model
        # exclude = ['price']  # Exclude the 'price' field from the form, as it will be calculated in the view

    design_requirement = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"accept":".bmp,.jpg,.jpeg,.png,.gif"}),
        required=False,
        label=("Add multiple design images"),
    )

    file_upload_required = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"accept":".pdf,.stl,.dcm,.html,.ply,.obj"}),
        required=False,
        label=("Add multiple file_upload_required"),
    )

    def clean_photos(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("design_requirement"):
            validate_image_file_extension(upload)

    def save_photos(self, order):
        """Process each uploaded image."""
        for upload in self.files.getlist("design_requirement"):
            photo = OrderGallery(order=order, image=upload, extension=upload.name.split('.')[1], title=upload.name)
            photo.save()
        for file in self.files.getlist("file_upload_required"):
            required_files = OrderGallery(order=order, image=file, extension=file.name.split('.')[1], title=file.name)
            print(required_files.title)
            required_files.save()


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_('Email'), max_length=250, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
        label=_("Email"),
    )