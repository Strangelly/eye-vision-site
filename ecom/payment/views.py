from django.shortcuts import get_object_or_404, render, redirect
from cart.cart import Cart
from payment.models import ShippingAddress, Order, OrderItem
from payment.forms import ShippingForm
from django.contrib import messages

def success(request):
    return render(request, 'pay/success.html', {})

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

    
    