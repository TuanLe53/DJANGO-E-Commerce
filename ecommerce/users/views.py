from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Credentials Invalid")
            return redirect("/login")
            
    return render(request, "users/login.html")

@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")

def register(request):
    if request.method =="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect("/register")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Name Already Taken")
                return redirect("/register")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                
                user_login = auth.authenticate(username=username, password=password1)
                auth.login(request, user_login)
                
                return redirect("/")
        else:
            messages.info(request, "Password not matching")
            return redirect("/register")
    
    return render(request, "users/register.html")