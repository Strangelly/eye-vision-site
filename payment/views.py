from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
import requests
import uuid
from cart.cart import Cart
from payment.models import ShippingAddress, Order, OrderItem
from payment.forms import ShippingForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def success(request):
    return render(request, 'pay/success.html', {})

@csrf_exempt
def payment_fail(request):
    return render(request, 'pay/payment_fail.html', {})

@csrf_exempt
def payment_cancel(request):
    return render(request, 'pay/payment_cancel.html', {})

def checkout(request):
    cart = Cart(request)
    items = cart.get_cart_items()
    total = cart.get_total_price()
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "pay/checkout.html", {"items": items,"total": total, "shipping_form": shipping_form})
    else:
        return render(request, "pay/checkout.html", {"items": items,"total": total})

def process_order(request):
    if request.method == 'POST':
        # Get cart and validate it's not empty
        cart = Cart(request)
        cart_items = cart.get_cart_items()
        total_price = cart.get_total_price()
        
        if not cart_items:
            messages.warning(request, "Your cart is empty")
            return redirect('checkout')
        
        # Validate and process the shipping form
        if request.user.is_authenticated:
            shipping_address = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_address)
        else:
            shipping_form = ShippingForm(request.POST or None)
        
        if shipping_form.is_valid():
            # Save the shipping address
            shipping_address = shipping_form.save(commit=False)
            if request.user.is_authenticated:
                shipping_address.user = request.user
            shipping_address.save()
            
            # Create the order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=shipping_address.shipping_full_name,
                email=shipping_address.shipping_email,
                total_price=total_price,
                shipping_address=shipping_address
            )
            
            # Create order items from cart
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            
            # Clear the cart
            cart.clear()
            
            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please fill in all required fields correctly")
            return redirect('home')
    else:
        messages.error(request, "Access Denied")
        return redirect('home')
    
def shipment_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        shipped_orders = Order.objects.filter(shipped=True).order_by('-date_shipped')
        unshipped_orders = Order.objects.filter(shipped=False).order_by('-created_at')

        if request.method == "POST":
            item_id = request.POST.get("num")
            status = request.POST.get("shipping_status")

            order = get_object_or_404(Order, id=item_id)

            if status == "true":
                order.shipped = True

            else:
                order.shipped = False

            order.save()            
            messages.success(request, "Shipping status updated successfully")
        
            return redirect('home')
        return render(request, 'pay/shipment_dash.html', {'shipped_orders': shipped_orders, 'unshipped_orders': unshipped_orders})

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order=pk)
    
    return render(request, 'pay/orders.html', {'orders': orders, 'order_items': order_items})

    
def initiate_payment(request):
    url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"

    data = {
        "store_id": "grief69a004a1555f5",
        "store_passwd": "grief69a004a1555f5@ssl",
        "total_amount": 100,
        "currency": "BDT",
        "tran_id": str(uuid.uuid4()),  # must be unique
        "success_url": "http://127.0.0.1:8000/payment/success/",
        "fail_url": "http://127.0.0.1:8000/payment/fail/",
        "cancel_url": "http://127.0.0.1:8000/payment/cancel/",
        "emi_option": 0,
        "cus_name": "Test User",
        "cus_email": "test@email.com",
        "cus_phone": "01700000000",
        "shipping_method": "NO",
        "product_name": "Test Product",
        "product_category": "Ecommerce",
        "product_profile": "general",
    }

    response = requests.post(url, data=data)
    res_data = response.json()

    # redirect user to payment page
    if res_data.get("status") == "SUCCESS":
        return redirect(res_data["GatewayPageURL"])
    else:
        return redirect("payment_failed")