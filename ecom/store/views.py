from itertools import product
import re
from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    products = Product.objects.all()
    
    # Get a single featured product - you can change the selection method:
    # Option 1: Get the first product
    featured_product = Product.objects.first()
    
    # Option 2: Get the last product
    # featured_product = Product.objects.last()
    
    # Option 3: Get a product by ID
    # featured_product = Product.objects.get(id=1)
    
    # Option 4: Get a product by ID with error handling
    # featured_product = get_object_or_404(Product, id=1)
    
    # Option 5: Get a random product (if you want to show different products)
    # import random
    # all_products = list(Product.objects.all())
    # featured_product = random.choice(all_products) if all_products else None
    
    context = {
        'products': products,
        'featured_product': featured_product,
        'user': request.user,
    }
    return render(request, 'home.html', context)

def collection(request):
    products = Product.objects.all()
    return render(request, 'collection.html', {'products':products})




