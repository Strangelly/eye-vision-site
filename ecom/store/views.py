from django.shortcuts import render
from .models import Product


def home(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'user': request.user,
    }
    return render(request, 'home.html', context)
