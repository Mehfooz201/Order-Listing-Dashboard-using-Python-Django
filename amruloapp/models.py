from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
from forex_python.converter import CurrencyRates
from django.db.models.signals import post_save
from django.dispatch import receiver



#Models here
class CompanyInformation(models.Model):
    company_name = models.CharField(max_length=200)
    company_phone = models.CharField(max_length=15)
    company_address = models.TextField()
    company_bank_name = models.CharField(max_length=200, blank=True, null=True)
    company_bank_account_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.company_name
    

class User(AbstractUser):
    
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, default='avatar.svg')
    phone = models.CharField(max_length=15, blank=True, null=True, default='')

    approval_status = models.BooleanField(default=True)
    
    company_information = models.ForeignKey(CompanyInformation, on_delete=models.SET_NULL, null=True, blank=True)

    country = models.CharField(max_length=50, null=True, blank=True)
    user_address = models.TextField(default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    


class FrameworkAgreement(models.Model):

    agreement_number = models.CharField(max_length=3, unique=True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    
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
    
    
    ORIGINAL_DATA_CHOICES = [
        ('Raw Scanned Data', 'Raw Scanned Data'),
    ]
    original_data = models.CharField(max_length=20, choices=ORIGINAL_DATA_CHOICES, default='Raw Scanned Data')
    
    DESIGN_PRINTING_CHOICES = [
        ('Design', 'Design'),
    ]
    design_printing = models.CharField(max_length=50, choices=DESIGN_PRINTING_CHOICES, default='Design')

    PRODUCT_TYPE_CHOICES = [
        ('Cobalt-chrome framework - Design Fee', 'Cobalt-chrome framework - Design Fee'),
    ]

    product_type = models.CharField(max_length=100, choices=PRODUCT_TYPE_CHOICES, default='Cobalt-chrome framework - Design Fee')


    PRODUCT_SUB_TYPE_CHOICES = [
        ('Anatomic Full Crown', 'Anatomic Full Crown '),
        ('Veneer ( Emax, Ivoclar)', 'Veneer ( Emax, Ivoclar)'),
        ('Inlay/Onlay', 'Inlay/Onlay'),
        ('Smile Creator', 'Smile Creator'),
        ('Acrylic Temporary Crowns', 'Acrylic Temporary Crowns'),
        ('Custom Implant Abutment', 'Custom Implant Abutment'),

        #Product others
        ('Cast Partial Denture Framework (upto 3 unit single arch)', 'Cast Partial Denture Framework (upto 3 unit single arch)'),
        ('Cast Partial Denture Framework (upto 6 unit single arch)', 'Cast Partial Denture Framework (upto 6 unit single arch)'),
        ('Cast Partial Denture Framework (upto 13 unit single arch)', 'Cast Partial Denture Framework (upto 13 unit single arch)'),

        ('Screw retained crown', 'Screw Retained Crown'),
        ('CO-CR framework', 'CO-CR framework'),
        ('Zirconia Framework', 'Zirconia Framework'),
        ('All on 4/6 implants', 'All on 4/6 implants'),
        ('Implant SLM malo bridge' ,'Implant SLM Malo Bridge '),
        ('Implant Hybrid Denture' ,'Implant Hybrid Denture'),
        ('Cast Partial Obturator' ,'Cast Partial Obturator'),
        ('Bridge Framework' ,'Bridge Framework'),
        ('Bite Splint' ,'Bite Splint'),
        ('Full Mouth Rehabilitation' ,'Full Mouth Rehabilitation'),
        ('Wax-up for smile correction' ,'Wax-up for smile correction '),

        #Product Materials
        ('Contact Model ( each quadrant )', 'Contact Model ( each quadrant )'),
        ('Contact Model with extra die  ( each quadrant )', 'Contact Model with extra die  ( each quadrant )'),
        ('Models with articulation (uppr/lower)', 'Models with articulation (uppr/lower)'),
        ('Study Model (Full Mouth)', 'Study Model (Full Mouth)'),
        ('Surgical guide', 'Surgical Guide'),
        
        # Add more options as needed
    ]

    
    product_sub_type = models.CharField(max_length=100, choices=PRODUCT_SUB_TYPE_CHOICES, default='Anatomic Full Crown')

  
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

    

    unit_of_measurement = models.CharField(max_length=10, choices=UNIT_CHOICES, default='PCS')
    CURRENCY_CHOICES = [
        ('USA', 'USD (Dollar)'),
        ('INR', 'INR (Indian Rupees)'),
        # Add more options as needed
    ]
    
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='USA')
    quantity = models.IntegerField()

    DELIVERY_TIMING_CHOICES = [
        ('12HRS', '12 HRS'),
        ('6HRS', '6 HRS'),
        ('2HRS', '2 HRS'),
    ]
    delivery_timing = models.CharField(max_length=10, choices=DELIVERY_TIMING_CHOICES, default='12HRS')


    design_requirement = models.FileField(upload_to='uploads/files/otherfiles', default='')
    file_upload_required = models.FileField(upload_to='uploads/files/stl-dcm-html')
    
    price = models.DecimalField(max_digits=10, decimal_places=2)



    #Remake Order Field
    # New fields for remaking
    remake_notes = models.TextField(blank=True)
    num_crowns = models.PositiveIntegerField(default=0)
    num_brackets = models.PositiveIntegerField(default=0)
    remake_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


    #CAD Design Result
    attachment_zip_rar = models.FileField(upload_to='uploads/files/zip-rar-attch/', null=True, blank=True)
    att_file_name = models.CharField(max_length=100, null=True, blank=True)
    


    

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


    def calculate_price(self):
        price_dict  = {
        '12HRS': {
                    'Anatomic Full Crown': 6.0, 
                    'Veneer ( Emax, Ivoclar)': 6.0, 
                    'Inlay/Onlay': 6.0, 
                    'Smile Creator': 6.0,
                    'Acrylic Temporary Crowns': 6.0, 
                    'Custom Implant Abutment': 7.0,

                    'Cast Partial Denture Framework (upto 3 unit single arch)' : 18.0,
                    'Cast Partial Denture Framework (upto 6 unit single arch)' : 18.0,
                    'Cast Partial Denture Framework (upto 13 unit single arch)' : 20.0,
                    'Screw retained crown' : 7.0,
                    'All on 4/6 implants' : 9.0,
                    'Implant SLM malo bridge' : 9.0,
                    'Implant Hybrid Denture' : 9.0,
                    'Cast Partial Obturator' : 9.0,
                    'Bridge Framework' : 7.0,
                    'Bite Splint' : 7.0,
                    'Full Mouth Rehabilitation' : 9.0,
                    'Wax-up for smile correction' : 9.0, 

                    'CO-CR framework' : 9.0,
                    'Zirconia Framework' : 9.0, 

                    'Contact Model ( each quadrant )' : 3.0,
                    'Contact Model with extra die  ( each quadrant )': 3.0,
                    'Models with articulation (uppr/lower)': 3.0,
                    'Study Model (Full Mouth)': 3.0,
                    'Surgical guide' : 40.0,
           
                  },

        '6HRS': {
                    'Anatomic Full Crown': 7.0,
                    'Veneer ( Emax, Ivoclar)': 7.0,
                    'Inlay/Onlay': 7.0,
                    'Smile Creator': 7.0,
                    'Acrylic Temporary Crowns': 7.0,
                    'Custom Implant Abutment': 9.0,

                    'Cast Partial Denture Framework (upto 3 unit single arch)' : 20.0,
                    'Cast Partial Denture Framework (upto 6 unit single arch)' : 20.0,
                    'Cast Partial Denture Framework (upto 13 unit single arch)' : 25.0,
                    'Screw retained crown' : 9.0,
                    'All on 4/6 implants' : 11.0,
                    'Implant SLM malo bridge' : 11.0,
                    'Implant Hybrid Denture' : 11.0,
                    'Cast Partial Obturator' : 11.0,
                    'Bridge Framework' : 9.0,
                    'Bite Splint' : 9.0,
                    'Full Mouth Rehabilitation' : 11.0,
                    'Wax-up for smile correction' : 11.0, 

                    'CO-CR framework' : 11.0,
                    'Zirconia Framework' : 11.0, 

                    'Contact Model ( each quadrant )' : 5.0,
                    'Contact Model with extra die  ( each quadrant )': 5.0,
                    'Models with articulation (uppr/lower)': 5.0,
                    'Study Model (Full Mouth)': 5.0,
                    'Surgical guide' : 36.0,
                 
                 },

        '2HRS': {
                    'Anatomic Full Crown': 9.0,
                    'Veneer ( Emax, Ivoclar)': 9.0,
                    'Inlay/Onlay': 9.0,
                    'Smile Creator': 9.0,
                    'Acrylic Temporary Crowns': 9.0,
                    'Custom Implant Abutment': 11.0,

                    'Cast Partial Denture Framework (upto 3 unit single arch)' : 0.0,
                    'Cast Partial Denture Framework (upto 6 unit single arch)' : 0.0,
                    'Cast Partial Denture Framework (upto 13 unit single arch)' : 0.0,
                    'Screw retained crown' : 11.0,
                    'All on 4/6 implants' : 15.0,
                    'Implant SLM malo bridge' : 15.0,
                    'Implant Hybrid Denture' : 15.0,
                    'Cast Partial Obturator' : 15.0,
                    'Bridge Framework' : 11.0,
                    'Bite Splint' : 11.0,
                    'Full Mouth Rehabilitation' : 15.0,
                    'Wax-up for smile correction' : 15.0, 

                    'CO-CR framework' : 15.0,
                    'Zirconia Framework' : 15.0, 

                    'Contact Model ( each quadrant )' : 7.0,
                    'Contact Model with extra die  ( each quadrant )': 7.0,
                    'Models with articulation (uppr/lower)': 7.0,
                    'Study Model (Full Mouth)': 7.0,
                    'Surgical guide' : 0.0,
                 }
    
    }

        # Get the base price for the selected product type and delivery timing from the price dictionary
        base_price = price_dict.get(self.delivery_timing, {}).get(self.product_sub_type)

        if base_price is None:
            # Set a default price (0 in this case) when the combination is not found in the dictionary
            base_price = 0

        total_price = base_price * self.quantity

        # Convert price to INR if currency is INR
        if self.currency == 'INR':
            c = CurrencyRates()
            inr_rate = c.get_rate('USD', 'INR')
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
        verbose_name_plural = "Orders"




# Signal handler for creating related records when a new user is added
@receiver(post_save, sender=User)
def create_user_related_records(sender, instance, created, **kwargs):
    if created:
        agreement = FrameworkAgreement.objects.create(customer=instance)
        instance.framework_agreement = agreement
        instance.save()

post_save.connect(create_user_related_records, sender=User)


