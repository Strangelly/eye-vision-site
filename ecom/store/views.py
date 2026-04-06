from pyexpat.errors import messages
import re
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product,Category
from django.db.models import Q
import random

def home(request):
    products = Product.objects.all()
    
    # Get a single featured product - you can change the selection method:
    # Option 1: Get the first product
    #featured_product = Product.objects.first()
    
    # Option 2: Get the last product
    # featured_product = Product.objects.last()
    
    # Option 3: Get a product by ID
    # featured_product = Product.objects.get(id=1)
    
    # Option 4: Get a product by ID with error handling
    # featured_product = get_object_or_404(Product, id=1)
    
    # Option 5: Get a random product (if you want to show different products)
    
    all_products = list(Product.objects.all())
    featured_product = random.choice(all_products) if all_products else None
    
    context = {
        'products': products,
        'featured_product': featured_product,
        'user': request.user,
    }
    return render(request, 'home.html', context)

def collection(request):
    products = Product.objects.all()
    return render(request, 'collection.html', {'products':products})

def item(request,pk):
    item = Product.objects.get(id=pk)
    return render(request, 'item.html', {'item':item})

# def category(request,foo):
#     foo = foo.replace('-',' ')
#     try:
#         category = Category.objects.get(name=foo)
#         items = Product.objects.filter(category=category)
#         return render(request, 'category.html', {'items':items})
#     except:
#         messages.success(request, ("That Category doesn't Exist"))
#         return redirect('home')

def category(request, name):
    category = Category.objects.get(name=name)
    products = Product.objects.filter(category=category)
    return render(request, "category.html", {
        "category": category,
        "products": products
    })
    

def search(request):
    query = request.GET.get("q")

    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    return render(request, "search.html", {
        "query": query,
        "products": products
    })



