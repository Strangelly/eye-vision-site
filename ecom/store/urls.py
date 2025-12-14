
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('collection/', views.collection, name='collection'),
    path('collection/<int:pk>', views.item, name='item'),
    path('category/<str:name>/', views.category, name="category"),
    path('search/', views.search , name="search"),
]
