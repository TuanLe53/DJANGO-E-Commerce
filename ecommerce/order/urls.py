from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("orders", views.orders, name="orders"),
    path("order/<int:pk>", views.order_detail, name="order_detail"),
]
