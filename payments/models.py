from django.db import models
from amruloapp.models import User,Order
# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    CURRENCY_CHOICES = [
        ('USA', 'USD (Dollar)'),
        ('INR', 'INR (Indian Rupees)'),
        # Add more options as needed
    ]
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='USA')
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id