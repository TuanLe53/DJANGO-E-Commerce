from django.db import models
from django.contrib.auth.models import User
from order.models import Order
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ("name",)
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField(default="", blank=True, null=True)
    quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pd_imgs")
    image = models.ImageField(upload_to="product_images")
    
    def __str__(self):
        return f"{self.product}'s image"
    
class OrderProduct(models.Model):
    ordered_quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products_list")
    total_price = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.product}"
    
    def get_total_price(self):
        return self.ordered_quantity * self.product.price
    
    def after_order(self):
        self.product.quantity -= self.ordered_quantity
        self.product.save()
        self.order.status = "Received"
        self.order.save()

class Wishlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    
    def __str__(self):
        return f"{self.customer}'s wishlist"