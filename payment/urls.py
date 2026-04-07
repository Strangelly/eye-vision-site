from django.urls import path
from . import views

urlpatterns = [
    path('success', views.success, name='success'),
    path('checkout', views.checkout, name='checkout'),
    path('process_order', views.process_order, name='process_order'),
    path('shipment_dash', views.shipment_dash, name='shipment_dash'),
    path('orders/<int:pk>', views.orders, name='orders'),
]
