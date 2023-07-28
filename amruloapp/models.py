from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
from forex_python.converter import CurrencyRates



#Models here

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, default='avatar.svg')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# models.py
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    ORDER_TYPE_CHOICES = [
        ('Regular', 'Regular order'),
        ('Simple', 'Simple Order'),
        ('Urgent', 'Urgent order'),
    ]
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    purchaser = models.CharField(max_length=100)
    salesman = models.CharField(max_length=100)
    production = models.CharField(max_length=100)
    requirements_remarks = models.TextField()

    # ... (other fields)
    order_date = models.DateField(default=timezone.now)

    #Section 02
    contacts = models.CharField(max_length=100)
    email = models.EmailField()
    COUNTRY_CHOICES = [
        ('USA', 'USA'),
        ('India', 'India'),
        ('Pakistan', 'Pakistan'),
        ('Bangladesh', 'Bangladesh'),
        ('Russia', 'Russia'),
        ('China', 'China'),
    ]
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    receiving_address = models.TextField()

    ORIGINAL_DATA_CHOICES = [
        ('Completed Design', 'Completed Design data'),
        ('Physical Impression', 'Physical Impression'),
        ('Raw Scanned Data', 'Raw Scanned Data'),
    ]
    original_data = models.CharField(max_length=20, choices=ORIGINAL_DATA_CHOICES)
    TYPESETTING_CHOICES = [
        ('Nesting & Slicing & Printing', 'Nesting & Slicing & Printing'),
        ('Nesting & Slicing', 'Nesting & Slicing'),
    ]
    typesetting_printing = models.CharField(max_length=50, choices=TYPESETTING_CHOICES)
    PRODUCT_TYPE_CHOICES = [
        ('Cobalt-chrome full contour Crown', 'Cobalt-chrome full contour Crown'),
        ('Cobalt-chrome framework', 'Cobalt-chrome framework'),
        ('Titanium Full Contour Crown (TC4)', 'Titanium Full Contour Crown (TC4)'),
        ('Titanium Framework (TC4)', 'Titanium Framework (TC4)'),
        # Add more options as needed
    ]
    product_type = models.CharField(max_length=100, choices=PRODUCT_TYPE_CHOICES)
    PRODUCT_SUB_TYPE_CHOICES = [
        ('Cast Partial Denture Framework (upto 3 unit single arch)', 'Cast Partial Denture Framework (upto 3 unit single arch)'),
        ('Cast Partial Denture Framework (upto 6 unit single arch)', 'Cast Partial Denture Framework (upto 6 unit single arch)'),
        ('Cast Partial Denture Framework (upto 13 unit single arch)', 'Cast Partial Denture Framework (upto 13 unit single arch)'),
        # Add more options as needed
    ]
    product_sub_type = models.CharField(max_length=100, choices=PRODUCT_SUB_TYPE_CHOICES)


    PRODUCT_MATERIAL= [
        ('OCOR', 'OCOR'),
        ('OCOR_2', 'OCOR_2'),
    ]

    product_material = models.CharField(max_length=50, choices=PRODUCT_MATERIAL)

    UNIT_CHOICES = [
        ('PCS', 'PCS'),
        # Add more options as needed
    ]
    unit_of_measurement = models.CharField(max_length=10, choices=UNIT_CHOICES)
    CURRENCY_CHOICES = [
        ('USA', 'USA'),
        ('INR', 'INR (Indian Rupees)'),
        # Add more options as needed
    ]
    
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='USD')
    quantity = models.IntegerField()
    num_of_files = models.IntegerField()
    DELIVERY_TIMING_CHOICES = [
        ('12HRS', '12 HRS'),
        ('6HRS', '6 HRS'),
        ('2HRS', '2 HRS'),
    ]
    delivery_timing = models.CharField(max_length=10, choices=DELIVERY_TIMING_CHOICES)
    file_upload_required = models.FileField(upload_to='uploads/files/')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    DELIVERY_TIMING_PRICES = {
        '12HRS': 10.0,  # Set the hourly rate for 12HRS delivery
        '6HRS': 15.0,   # Set the hourly rate for 6HRS delivery
        '2HRS': 20.0,   # Set the hourly rate for 2HRS delivery
    }

    def calculate_price(self):
        base_price = self.DELIVERY_TIMING_PRICES.get(self.delivery_timing, 0)
        total_price = base_price * self.quantity

        # Convert price to INR if currency is INR
        if self.currency == 'INR':
            c = CurrencyRates()
            inr_rate = c.get_rate('USD', 'INR')
            total_price = total_price * inr_rate

        return total_price
    

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.calculate_price()
        super(Order, self).save(*args, **kwargs)

    # ... (other fields)

    def __str__(self):
        currency_indicator = "$" if self.currency == 'USD' else "Rs."
        return f"Order {self.id} - {self.customer_name} ({currency_indicator}{self.price:.2f})"

    class Meta:
        verbose_name_plural = "Orders"
