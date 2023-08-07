from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Received", "Received"),
        ("Delivering", "Delivering"),
        ("Delivered", "Delivered")
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="New")
    total_price = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.customer}'s Order {self.id}"
    
    def get_total_price(self):
        return round(sum([x.total_price for x in self.products_list.all()]), 2)
    
    
class Address(models.Model):
    PAYMENT_METHODS_CHOICES = [
        ("COD", "COD"),
        ("Credit Card", "Credit Card"),
        ("Mobile Payments", "Mobile Payments")
    ]
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")    
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="address")
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHODS_CHOICES, default="COD")
    
    def __str__(self):
        return f"Address of {self.order}"