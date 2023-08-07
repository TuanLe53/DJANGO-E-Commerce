from django.contrib import admin
from .models import Product, ProductImages, Category, OrderProduct, Wishlist
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(OrderProduct)
admin.site.register(Wishlist)