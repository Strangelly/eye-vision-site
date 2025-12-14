from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    items = cart.get_cart_items()
    total = cart.get_total_price()

    return render(request, "c_summary.html", {"items": items,"total": total})

def cart_add(request):
    cart = Cart(request)

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity)
        cart_quantity = cart.__len__()
        messages.success(request, f"Added {product.name} to cart.")
        return JsonResponse({"cart_quantity": len(cart)})
    
    

def cart_delete(request):
    cart = Cart(request)

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        cart.remove(product)
        messages.success(request, f"Removed {product.name} from cart.")

        return JsonResponse({
            "success": True,
            "cart_quantity": len(cart),
            "cart_total": cart.get_total_price()
        })

def cart_update(request):
    cart = Cart(request)

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))

        product = get_object_or_404(Product, id=product_id)

        cart.update(product, quantity)

        return JsonResponse({
            "success": True,
            "cart_quantity": len(cart),
            "item_total": quantity * float(product.sale_price if product.is_sale else product.price),
            "cart_total": cart.get_total_price()
        })