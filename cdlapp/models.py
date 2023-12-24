from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
from forex_python.converter import CurrencyRates
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from products.models import (
    OriginalData,DesignPrinting,ProductType,ProductSubType,
    ProductMaterial,DeliveryTiming,Product
    )

from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin
from cdlapp.storage import OverwriteStorage
custom_store = OverwriteStorage()

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self,username,name,email,password=None):
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
        )   
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,name,username,email,password): 
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            name=name,
            password=password,
        )   
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class CompanyInformation(models.Model):
    company_name = models.CharField(max_length=200)
    company_phone = models.CharField(max_length=15)
    company_address = models.TextField()
    company_bank_name = models.CharField(max_length=200, blank=True, null=True)
    company_bank_account_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.company_name

class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=100,blank=True, null=True,)
    last_name = models.CharField(max_length=100,blank=True, null=True,)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=150,unique=True, null=True)
    avatar = models.ImageField(storage=custom_store,null=True, default='avatar.svg')
    phone = models.CharField(max_length=15, blank=True, null=True, default='')

    approval_status = models.BooleanField(default=True)
    
    company_information = models.ForeignKey(CompanyInformation, on_delete=models.SET_NULL, null=True, blank=True)

    country = models.CharField(max_length=50, null=True, blank=True)
    user_address = models.TextField(default='', null=True, blank=True)

    #user_password = models.CharField(max_length=50, blank=True, null=True, default='')
    #confirm_password = models.CharField(max_length=50, blank=True, null=True, default='')
    
    # Required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','username']
    
    objects = MyAccountManager()

    
    def __str__(self):
        return str(self.username)

    def has_module_perms(self, app_label):
        return self.is_admin


class FrameworkInformation(models.Model):
    cooperation_mode_content = models.TextField(blank=True, null=True)
    payment_method_content = models.TextField(blank=True, null=True)
    processing_quantity_content = models.TextField(blank=True, null=True)
    price_adjustment_content = models.TextField(blank=True, null=True)
    shipping_method_content = models.TextField(blank=True, null=True)
    product_acceptance_content = models.TextField(blank=True, null=True)
    number_management_content = models.TextField(blank=True, null=True)
    breach_contract_content = models.TextField(blank=True, null=True)
    force_majeure_content = models.TextField(blank=True, null=True)
    order_effect_content = models.TextField(blank=True, null=True)
    sign_confirmation_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Framework Agreement Information'


class FrameworkAgreement(models.Model):
    agreement_number = models.CharField(max_length=3, unique=True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    # frameinfo = models.ForeignKey(FrameworkInformation, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.agreement_number:
            self.agreement_number = self.generate_agreement_number()
        super(FrameworkAgreement, self).save(*args, **kwargs)

    def generate_agreement_number(self):
        last_agreement = FrameworkAgreement.objects.order_by('agreement_number').last()
        if last_agreement:
            last_number = int(last_agreement.agreement_number)
            new_number = f"{last_number + 1:03}"
        else:
            new_number = "001"
        return new_number
    
    def __str__(self):
        return self.agreement_number
    
    class Meta:
        verbose_name_plural = "Framework Agreements"


# models.py
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('review', 'Review'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    order_status = models.CharField(
        max_length=12, choices=ORDER_STATUS_CHOICES, null=True, blank=True, default='review')

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link the order with the user
    company_information = models.ForeignKey(CompanyInformation, on_delete=models.SET_NULL, null=True, blank=True)
    framework_agreement = models.ForeignKey(FrameworkAgreement, on_delete=models.SET_NULL, null=True, blank=True)
    
    order_number = models.AutoField(primary_key=True)  # Auto-generated order number
    customer_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    ORDER_TYPE_CHOICES = [
        ('Regular', 'Regular Order'),
        ('Simple', 'Sample Order'),
        ('Urgent', 'Urgent order'),
    ]
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default='Regular')
    purchaser = models.CharField(max_length=100, blank=True, null=True)
    salesman = models.CharField(max_length=100, blank=True, null=True)
    requirements_remarks = models.TextField(blank=True, null=True)

    # ... (other fields)
    order_date = models.DateField(default=timezone.now, null=True, blank=True)
    def formatted_order_date(self):
        return self.order_date.strftime('%Y-%m-%d 00:00')
    
    original_data = models.ForeignKey(OriginalData, on_delete=models.CASCADE)
    design_printing = models.ForeignKey(DesignPrinting, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    product_sub_type = models.ForeignKey(ProductSubType, on_delete=models.CASCADE)
    product_material = models.ForeignKey(ProductMaterial, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    delivery_timing = models.ForeignKey(DeliveryTiming, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    CURRENCY_CHOICES = [
        ('USA', 'USD (Dollar)'),
        ('INR', 'INR (Indian Rupees)'),
        # Add more options as needed
    ]

    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='USA')
    design_requirement = models.FileField(upload_to='uploads/files/otherfiles', blank=True)
    file_upload_required = models.FileField(upload_to='uploads/files/stl-dcm-html', blank=True)

    #Remake Order Field
    # New fields for remaking
    remake_notes = models.TextField(blank=True)
    num_crowns = models.PositiveIntegerField(default=0)
    num_brackets = models.PositiveIntegerField(default=0)
    remake_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


    #CAD Design Result
    attachment_zip_rar = models.FileField(upload_to='uploads/files/zip-rar-attch/', null=True, blank=True)
    att_file_name = models.CharField(max_length=100, null=True, blank=True)

    is_ordered = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        if not self.framework_agreement_id:
            recent_agreement = FrameworkAgreement.objects.filter(customer=self.user).order_by('-id').first()
            if recent_agreement:
                self.framework_agreement = recent_agreement
            
        if not self.price:
            self.price = self.calculate_price()

        # Calculate total amount including original price and remake charges
        self.price = self.price + self.remake_price
        super(Order, self).save(*args, **kwargs)

    @property
    def gallery(self):
        data = []
        gallery = OrderGallery.objects.all().filter(order_id=self.pk)
        for i in gallery:
            data.append({"title":i.title,"url":i.image.url,"extension":i.extension})
        return data

    @property
    def calculate_price(self):
        delivery_timing = DeliveryTiming.objects.all()
        products = Product.objects.all()
        data_product_price = []
        for j in delivery_timing:
            data_product_price.append({str(j.id):{str(i.product_sub_type.id):i.product_12hrs_price.delivery_timing.name == j.name and float(i.product_12hrs_price.price) or i.product_6hrs_price.delivery_timing.name == j.name and float(i.product_6hrs_price.price) or i.product_2hrs_price.delivery_timing.name == j.name and float(i.product_2hrs_price.price) for i in products }})

        format_data1 = str(data_product_price).replace('[','')
        format_data2 = format_data1.replace(']','')
        format_data3 = format_data2.replace("}}, {","}, ")
        format_data4 = format_data3.replace("}}, {","}, ")
        format_data5 = format_data4.replace("'","\"")
        format_data6 = str(format_data5).replace("\'"," ")
        price_dict  = eval(format_data6)
        # Get the base price for the selected product type and delivery timing from the price dictionary
        base_price = price_dict.get(str(self.delivery_timing.id), {}).get(str(self.product_sub_type.id))

        if base_price is None:
            # Set a default price (0 in this case) when the combination is not found in the dictionary
            base_price = 0

        total_price = base_price * self.quantity

        inr_rate = 0
        # Fetch the actual exchange rate for INR
        try:
            c = CurrencyRates()
            inr_rate = c.get_rate('USA', 'INR')
        except:
            # Handle the error gracefully, e.g., use a default exchange rate
            inr_rate = 83.12  # You can use a default value here or handle the error as per your requirement

        # Convert price to INR if currency is INR
        if self.currency == 'INR':
            total_price *= inr_rate

        return total_price

    def save(self, *args, **kwargs):
        if not self.framework_agreement_id:
            recent_agreement = FrameworkAgreement.objects.filter(customer=self.user).order_by('-id').first()
            if recent_agreement:
                self.framework_agreement = recent_agreement

        if not self.price:
            self.price = self.calculate_price()
        super(Order, self).save(*args, **kwargs)

    # ... (other fields)

    def __str__(self):
        currency_indicator = "$" if self.currency == 'USD' else "Rs."
        return f"Order {self.order_number} - {self.customer_name} ({currency_indicator}{self.price:.2f})"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderGallery(models.Model):
    order = models.ForeignKey(Order, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    extension = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='uploads/files/gallery', blank=True, max_length=255)

    def __str__(self):
        return str(self.image)
    class Meta:
        verbose_name = "Order Gallery"
        verbose_name_plural = "Orders Gallery"




# Signal handler for creating related records when a new user is added
@receiver(post_save, sender=User)
def create_user_related_records(sender, instance, created, **kwargs):
    if created:
        agreement = FrameworkAgreement.objects.create(customer=instance)
        instance.framework_agreement = agreement
        instance.save()

post_save.connect(create_user_related_records, sender=User)


#Email Sending to users
@receiver(post_save, sender=User)
def send_user_registration_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Confident Dental Laboratory (Pvt.) Ltd"
        
        # Get the absolute URL for the homepage
        homepage_url = "https://design.confidentlab.com/"  # Replace with your actual website URL
        
        message = (
            f"Hello {instance.username},\n\n"
            f"Thank you for registering with our Company. Here are your login details:\n\n"
            f"Customer Username: {instance.username}\n"
            f"Email: {instance.email}\n"
            f"Password: {instance.password}\n\n"
            f"You can log in to our website using these credentials.\n"
            f"Please visit our website at: {homepage_url}\n\n"  # Include the URL here
            f"Best regards,\nConfident Dental Laboratory (Pvt.) Ltd"
        )
        from_email = "admin@design.confidentlab.com"  # Change to your admin's email address
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)

post_save.connect(send_user_registration_email, sender=User)
