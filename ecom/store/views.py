from django.shortcuts import render, redirect
from django.contrib.auth import logout

def home(request):
    if request.user.is_superuser:
        logout(request)
        redirect("/")
    return render(request, 'home.html', {})
