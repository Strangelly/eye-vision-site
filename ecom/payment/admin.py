from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)   
admin.site.register(Order)    
admin.site.register(OrderItem) 

# OrderItem inline 
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # no extra slots for new items

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['created_at']
    fields = ['user', 'full_name', 'email', 'total_price', 'shipping_address', 'created_at', 'shipped', 'date_shipped']
    inlines = [OrderItemInline]

admin.site.unregister(Order)  

admin.site.register(Order, OrderAdmin)