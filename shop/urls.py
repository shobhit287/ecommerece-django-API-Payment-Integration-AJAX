from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('product/<int:p_id>',views.product,name="cart"),
    path('about',views.about,name="about"),
    path('search',views.search,name="search"),
    path('contactus',views.contactus,name="contactus"),
    path('checkout',views.checkout,name="checkout"),
    path('tracker',views.tracker,name="tracker"),
    path('handlerequest',views.handlerequest,name="handlerequest")
    
]