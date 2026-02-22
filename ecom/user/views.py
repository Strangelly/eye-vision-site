from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, User_form
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache

from payment.models import ShippingAddress
from payment.forms import ShippingForm

import random
from .models import CustomUser, Profile
import re


# Create your views here.
def login_required_message(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You need to login to view this page.")
            print(request.path)
            return redirect(f"/user/login/?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper


def is_pwd_valid(pwd1, pwd2):
    errors = {}
    if pwd1 != pwd2:
        errors["confirm_password"] = "password did not match"
        return errors
    if len(pwd1) < 8:
        errors["password"] = "Password must be at least 8 characters long."
        return errors

    if not re.search(r"[A-Za-z]", pwd1):
        errors["password"] = "Password must contain at least one letter."

    if not re.search(r"\d", pwd1):
        errors["password"] = "Password must contain at least one digit."

    if not re.search(r"[^\w]", pwd1):
        errors["password"] = "Password must contain at least one symbol."
    
    return errors


def make_otp(mobile):
    otp = str(random.randint(100000, 999999))
    hased_otp = make_password(otp)
    cache.set(f"otp:{mobile}", hased_otp, timeout=120)
    print(otp)


@login_required_message
def user(request):
    if "forgot_paa" in request.session:
        del request.session["forgot_paa"]
    if "mobile" in request.session:
        del request.session["mobile"]
    user = request.user
    shipping_info = ShippingAddress.objects.filter(user=user).first()
    return render(request, "user/user.html",{
            "user": user,
            "shipping_info": shipping_info
        })




def login_user(request):
    if "forgot_paa" in request.session:
        del request.session["forgot_paa"]
    if "mobile" in request.session:
        del request.session["mobile"]
    if request.user.is_authenticated:
        messages.error(request, "already login")
        return redirect("/")
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST) 
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not request.GET.get('next'):
                messages.success(request, "Login successfull")
            next_url = request.GET.get('next') or '/'
            return redirect(next_url)
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
            if request.session.get("forgot_paa"):
                return redirect("new_password")
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


@login_required_message
def update_profile(request):
    if not request.user.is_varified:
        messages.warning(request, "You need to verify your number to edit your profile")
        return redirect("user")
    current_user = Profile.objects.get(user__id=request.user.id)
    shipping_user = ShippingAddress.objects.get(id=request.user.id)
        
    form = User_form(request.POST or None, instance=current_user)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)  
    if shipping_form.is_valid():
        shipping_form.save()
        messages.success(request, "Profile updated successfully")
        return redirect("user")
    return render(request, "user/update_profile.html", {"form": form, "shipping_form": shipping_form})
    


def forgot_password_mobile(request):
    if request.user.is_authenticated:
        messages.warning(request, "already login")
        return redirect("/")
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        user = CustomUser.objects.filter(mobile = mobile)
        if user:
            request.session["forgot_paa"] = True
            request.session["mobile"] = mobile
            return redirect("otp")
        else:
            messages.error(request, "mobile not found")
    return render(request, "user/fogot_password_mobile.html")


def new_password(request):
    if "forgot_paa" in request.session:
        if request.method == "POST":
            pwd1 = request.POST.get("password")
            pwd2 = request.POST.get("confirm_password")
            errors = is_pwd_valid(pwd1, pwd2)
            if not errors:
                mobile = request.session.get("mobile")
                user = CustomUser.objects.get(mobile = mobile)
                user.set_password(pwd1)
                user.save()
                del request.session["forgot_paa"]
                messages.success(request, "password reset succesfull now login")
                return redirect("login")
            else:
                return render(request, "user/new_password.html", {"errors": errors})
        return render(request, "user/new_password.html")
    else:
        messages.warning(request, "unable to access this page now")
        return redirect("/")


