from django.urls import path
from . import views

urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('process_order', views.process_order, name='process_order'),
    path('shipment_dash', views.shipment_dash, name='shipment_dash'),
    path('orders/<int:pk>', views.orders, name='orders'),
    path('pay', views.initiate_payment, name='pay'),
    path('success/', views.success, name='success'),
    path('fail/', views.payment_fail, name='payment_fail'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
]
