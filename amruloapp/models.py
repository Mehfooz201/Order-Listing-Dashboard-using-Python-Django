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
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# models.py
class Order(models.Model):
    order_number = models.AutoField(primary_key=True)  # Auto-generated order number
    customer_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    ORDER_TYPE_CHOICES = [
        ('Regular', 'Regular Order'),
        ('Simple', 'Sample Order'),
        ('Urgent', 'Urgent order'),
    ]
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default='Regular')
    purchaser = models.CharField(max_length=100)
    salesman = models.CharField(max_length=100)
    requirements_remarks = models.TextField()

    # ... (other fields)
    order_date = models.DateField(default=timezone.now, null=True, blank=True)

    #Section 02
    contacts = models.CharField(max_length=100)
    email = models.EmailField()
    COUNTRY_CHOICES = [
        ('India', 'India'),
        ('USA', 'USA'),
        ('Pakistan', 'Pakistan'),
        ('Bangladesh', 'Bangladesh'),
        ('Russia', 'Russia'),
        ('China', 'China'),
    ]
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES, default='India')
    receiving_address = models.TextField()

    ORDER_STATUS_CHOICES = [
        ('active', 'Active'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
        ('modification', 'Modification'),
    ]

    order_status = models.CharField(
        max_length=12, choices=ORDER_STATUS_CHOICES, null=True, blank=True, default='active')

    ORIGINAL_DATA_CHOICES = [
        ('Completed Design', 'Completed Design Data'),
        ('Physical Impression', 'Physical Impression'),
        ('Raw Scanned Data', 'Raw Scanned Data'),
    ]
    original_data = models.CharField(max_length=20, choices=ORIGINAL_DATA_CHOICES, default='Completed Design')
    
    TYPESETTING_CHOICES = [
        ('Nesting & Slicing & Printing', 'Nesting & Slicing & Printing'),
        ('Nesting & Slicing', 'Nesting & Slicing'),
    ]
    typesetting_printing = models.CharField(max_length=50, choices=TYPESETTING_CHOICES, default='Nesting & Slicing & Printing')

    PRODUCT_TYPE_CHOICES = [
        ('Anatomic Full Crown', 'Anatomic Full Crown '),
        ('Veneer ( Emax, Ivoclar)', 'Veneer ( Emax, Ivoclar)'),
        ('Inlay/Onlay', 'Inlay/Onlay'),
        ('Smile Creator', 'Smile Creator'),
        ('Acrylic Temporary Crowns', 'Acrylic Temporary Crowns'),
        ('Inlay/Onlay', 'Inlay/Onlay'),
        ('Custom Implant Abutment', 'Custom Implant Abutment'),
        ('Cobalt-chrome framework', 'Cobalt-chrome framework'),
        ('Titanium Full Contour Crown (TC4)', 'Titanium Full Contour Crown (TC4)'),
        ('Titanium Framework (TC4)', 'Titanium Framework (TC4)'),
        # Add more options as needed
    ]

    product_type = models.CharField(max_length=100, choices=PRODUCT_TYPE_CHOICES, default='Anatomic Full Crown')
    PRODUCT_SUB_TYPE_CHOICES = [
        ('Cast Partial Denture Framework (upto 3 unit single arch)', 'Cast Partial Denture Framework (upto 3 unit single arch)'),
        ('Cast Partial Denture Framework (upto 6 unit single arch)', 'Cast Partial Denture Framework (upto 6 unit single arch)'),
        ('Cast Partial Denture Framework (upto 13 unit single arch)', 'Cast Partial Denture Framework (upto 13 unit single arch)'),

        ('Screw retained crown', 'Screw Retained Crown'),
        ('All on 4/6 implants', 'All on 4/6 implants'),
        ('Implant SLM malo bridge' ,'Implant SLM Malo Bridge '),
        ('Implant Hybrid Denture' ,'Implant Hybrid Denture'),
        ('Cast Partial Obturator' ,'Cast Partial Obturator'),
        ('Bridge Framework' ,'Bridge Framework'),
        ('Bite Splint' ,'Bite Splint'),
        ('Full Mouth Rehabilitation' ,'Full Mouth Rehabilitation'),
        ('Wax-up for smile correction' ,'Wax-up for smile correction '),
    ]
    product_sub_type = models.CharField(max_length=100, choices=PRODUCT_SUB_TYPE_CHOICES, default='Cast Partial Denture Framework (upto 3 unit single arch)')


    PRODUCT_MATERIAL= [
        ('OCOR', 'OCOR'),
        ('Metal ', 'Metal'),
        ('Resin', 'Resin'),
        ('Zirconia / Metal / PMMA ', 'Zirconia / Metal / PMMA '),
        ('Zirconia / Emax', 'Zirconia / Emax'),
        ('Wax' , 'Wax'),
        ('PMMA', 'PMMA'),
        ('Zirconia / Metal', 'Zirconia / Metal ')
    ]

    product_material = models.CharField(max_length=50, choices=PRODUCT_MATERIAL, default='OCOR')

    UNIT_CHOICES = [
        ('PCS', 'PCS'),
        # Add more options as needed
    ]

    MODEL_DESIGN =[
        ('Contact Model ( each quadrant )', 'Contact Model ( each quadrant )'),
        ('Contact Model with extra die  ( each quadrant )', 'Contact Model with extra die  ( each quadrant )'),
        ('Models with articulation (uppr/lower)', 'Models with articulation (uppr/lower)'),
        ('Study Model (Full Mouth)', 'Study Model (Full Mouth)'),
        ('Surgical guide ', 'Surgical Guide'),
    ]
    model_design = models.CharField(max_length=50, choices=MODEL_DESIGN, default='Contact Model ( each quadrant )')


    unit_of_measurement = models.CharField(max_length=10, choices=UNIT_CHOICES, default='PCS')
    CURRENCY_CHOICES = [
        ('USA', 'USA ($)'),
        ('INR', 'INR (Indian Rupees)'),
        # Add more options as needed
    ]
    
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='INR')
    quantity = models.IntegerField()

    DELIVERY_TIMING_CHOICES = [
        ('12HRS', '12 HRS'),
        ('6HRS', '6 HRS'),
        ('2HRS', '2 HRS'),
    ]
    delivery_timing = models.CharField(max_length=10, choices=DELIVERY_TIMING_CHOICES, default='12HRS')
    file_upload_required = models.FileField(upload_to='uploads/files/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

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
        return f"Order {self.order_number} - {self.customer_name} ({currency_indicator}{self.price:.2f})"

    class Meta:
        verbose_name_plural = "Orders"
