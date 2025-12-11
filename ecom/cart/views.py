from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse


def cart_summary(request):
    cart = Cart(request)
    cart_items = cart.get_prods() 
    return render(request, "c_summary.html", {"cart_items": cart_items})

def cart_add(request):
    cart = Cart(request)
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)

        cart_quantity = cart.__len__()
        
        return JsonResponse({"cart_quantity": len(cart)})
    
    

def cart_delete(request):
    pass

def cart_update(request):
    pass
