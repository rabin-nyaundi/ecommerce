from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html',
    { 'products': products})

def cart_view(request):
    return render(request, 'shop/cart.html')

def checkout_view(request):
    return render(request, 'shop/checkout.html')