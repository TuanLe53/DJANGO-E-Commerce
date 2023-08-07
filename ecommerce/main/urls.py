from django.urls import path
from . import views

app_name= "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("store/<int:pk>", views.store, name="store"),
    path("add", views.add_product, name="add"),
    path("product/<int:pk>", views.pd_detail, name="detail"),
    path("wishlist", views.userwishlist, name="wishlist"),
    path("add-to-wishlist/<int:pk>", views.add_to_wishlist, name="add_to_wishlist"),
]