from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddProductForm, ImageForm
from .models import ProductImages, Product, OrderProduct, Wishlist
from order.models import Order
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    
    def group_product(category_id):
        pd_by_category = Product.objects.filter(category=category_id)
        grouped = []
        pd_iter = iter(pd_by_category)
        for item in pd_iter:
            try:
                group = [item, next(pd_iter), next(pd_iter), next(pd_iter)]
                grouped.append(group)
            except:
                pass
        return grouped
    
    section_1 = group_product(5)
    section_2 = group_product(6)
    section_3 = group_product(7)

    context = {
        "section_1": section_1,
        "section_2": section_2,
        "section_3": section_3,
    }
    
    return render(request, "main/home.html", context)

def store(request, pk):
    owner = User.objects.get(id=pk)
    pd_list = Product.objects.filter(owner=owner)
    
    context = {
       "pd_list": pd_list,
       "owner": owner
    }
    
    return render(request, "main/store.html", context)

@login_required
def add_product(request):
    ImageFormSet = modelformset_factory(ProductImages, form=ImageForm, extra=5)
    
    if request.method == "POST":
        form = AddProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImages.objects.none())

        if form.is_valid() and formset.is_valid():
            pd = form.save(commit=False)
            pd.owner = request.user
            pd.save()
            
            for form in formset.cleaned_data:
                if form:
                    image = form["image"]
                    photo = ProductImages(product=pd, image=image)
                    photo.save()
            return redirect(f"/store/{request.user.id}")
        else:
            return redirect("/add")
    
    else:
        form = AddProductForm()
        formset = ImageFormSet(queryset=ProductImages.objects.none())
        
    context ={
        "form": form,
        "formset": formset,
    }
    
    return render(request, "main/add.html", context)

def pd_detail(request, pk):
    pd = Product.objects.get(id=pk)
    user = request.user
    
    if request.method == "POST":
        if user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=user, status="New")
            order_product = OrderProduct.objects.create(product=pd, ordered_quantity=int(request.POST["quantity"]), order=order)
            
            order_product.total_price = order_product.get_total_price()
            order_product.save()
            
            order.total_price = order.get_total_price()
            order.save()
            
            messages.success(request, "Product was successfully added to your order")
        else:
            messages.info(request, "You need to login to add product")
            return redirect("/login")
        
    context = {
        "product": pd,
    }
    
    return render(request, "main/detail.html", context)

@login_required
def userwishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(customer=request.user)

    context = {
        "wishlist": wishlist,
    }
    
    return render(request, "main/wishlist.html", context)

def add_to_wishlist(request, pk):
    user = request.user
    pd = Product.objects.get(id=pk)
    
    if user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(customer=user)
        wishlist.products.add(pd)
        messages.success(request, "Product was successfully added to your wishlist")
        return redirect(f"/product/{pk}")
    else:
        messages.info(request, "You need to login to add product")
        return redirect("/login")