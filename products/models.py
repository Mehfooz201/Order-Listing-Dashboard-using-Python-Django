from django.db import models

# Create your models here.
class OriginalData(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name
class DesignPrinting(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name
class ProductType(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name
class ProductSubType(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name
class ProductMaterial(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name
class UnitOfMeasurement(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name
class DeliveryTiming(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name
class Product12HrsPrice(models.Model):
    product_sub_type = models.ForeignKey(ProductSubType, on_delete=models.CASCADE)
    delivery_timing = models.ForeignKey(DeliveryTiming, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return str(self.price)
class Product6HrsPrice(models.Model):
    product_sub_type = models.ForeignKey(ProductSubType, on_delete=models.CASCADE)
    delivery_timing = models.ForeignKey(DeliveryTiming, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return str(self.price)
class Product2HrsPrice(models.Model):
    product_sub_type = models.ForeignKey(ProductSubType, on_delete=models.CASCADE)
    delivery_timing = models.ForeignKey(DeliveryTiming, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return str(self.price)

class Product(models.Model):
    original_data = models.ForeignKey(OriginalData, on_delete=models.CASCADE)
    design_printing = models.ForeignKey(DesignPrinting, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    product_sub_type = models.ForeignKey(ProductSubType, on_delete=models.CASCADE)
    product_material = models.ForeignKey(ProductMaterial, on_delete=models.CASCADE)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE)
    product_12hrs_price = models.ForeignKey(Product12HrsPrice, on_delete=models.CASCADE)
    product_6hrs_price = models.ForeignKey(Product6HrsPrice, on_delete=models.CASCADE)
    product_2hrs_price = models.ForeignKey(Product2HrsPrice, on_delete=models.CASCADE)
    group1 = models.BooleanField(default=False)
    group2 = models.BooleanField(default=False)
    group3 = models.BooleanField(default=False)
    def __str__(self):
        return self.product_sub_type.name