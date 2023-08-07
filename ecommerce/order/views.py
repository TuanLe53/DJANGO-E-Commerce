from django.shortcuts import render, redirect
from .models import Order, Address
from .forms import AddressForm
# Create your views here.
def orders(request):
    user = request.user
    orders_list = [x for x in Order.objects.filter(customer=user) if x.status != "New"]
    new_order, created = Order.objects.get_or_create(customer=user, status="New")
    
    if request.method =="POST":
        form = AddressForm(request.POST)
        if form.is_valid() and new_order.products_list.all():
            for pd in new_order.products_list.all():
                pd.after_order()
                
            address = form.save(commit=False)
            address.order = new_order
            address.customer = user
            address.save()
            
            return redirect("/orders")
        else:
            return redirect("/orders")
    
    else:
        form = AddressForm()
        
    context ={
        "orders": orders_list,
        "new_order": new_order,
        "form": form,
    }
    
    return render(request, "order/orders.html", context)

def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    address = Address.objects.get(order=order)

    context = {
        "order": order,
        "address": address,
    } 
    
    return render(request, "order/order_detail.html", context)