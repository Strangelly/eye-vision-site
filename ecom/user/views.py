from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, User_form
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
import random
from .models import CustomUser, Profile

# Create your views here.
def make_otp(mobile):
    otp = str(random.randint(100000, 999999))
    hased_otp = make_password(otp)
    cache.set(f"otp:{mobile}", hased_otp, timeout=120)
    print(otp)

def user(request):
    if request.user.is_superuser or not request.user.is_authenticated:
        if request.user.is_superuser:
            logout(request)
        messages.error(request, "please login")
        return redirect("/")
    user = request.user
    return render(request, "user/user.html", {"user": user})



def login_user(request):
    if request.user.is_authenticated:
        messages.error(request, "already login")
        return redirect("/")
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST) 
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                messages.error(request, "superuser can`t login here. goto admin page to login as superuser" )
                return redirect("/")
            login(request, user)
            messages.success(request, "Login successfull" )
            return redirect("/")
        else:
            messages.error(request, "Invalid Email or Password")
    else:
        form = AuthenticationForm()

    return render(request, "user/login.html", {"form":form})

def logout_user(request):
    logout(request)
    messages.success(request, "Logout successfull" )
    return redirect("/")

def registration_user(request):
    if request.user.is_authenticated:
        messages.error(request, "already login. please logout to register" )
        return redirect('/')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            mobile = form.cleaned_data.get("mobile")
            request.session["mobile"] = mobile
            return redirect("otp")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "user/registration.html", {"form": form})


def otp_varification(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user.is_varified:
                messages.error(request, "already varified")
                return redirect("/")
            mobile = request.user.mobile
        elif request.session.get("mobile"):
            mobile = request.session.get("mobile")
        otp = request.POST.get("otp")
        hased = cache.get(f"otp:{mobile}")
        if hased and check_password(otp, hased):
            messages.success(request, "verification Successfull")
            user = CustomUser.objects.get(mobile=mobile)
            user.is_varified = True
            user.save()
            cache.delete(f"otp:{mobile}")
            return redirect("/")
        else:
            messages.error(request, "Invalid otp")
    else:
        if request.user.is_authenticated:
            if request.user.is_varified:
                messages.error(request, "already varified")
                return redirect("/")
            mobile = request.user.mobile
        elif request.session.get("mobile"):
            mobile = request.session.get("mobile")
        else:
            messages.error(request, "please login or register")
            return redirect("/")
        make_otp(mobile)    

    return render(request, "user/otp_varification.html")


def update_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "you have to login to view this page" )
        return redirect('/')
    profile = get_object_or_404(Profile, user__mobile =request.user.mobile)
    if request.method == "POST":
        form = User_form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "update succesfull")
            return redirect("user")
    form = User_form(instance=profile)
    return render(request, "user/update_profile.html", {"form":form})