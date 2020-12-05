from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.
def index(request):
    cat = Category.objects.all()
    products = Product.objects.all()  
    
    if request.user.is_authenticated:
        user = request.user.customer
        order, created = Order.objects.get_or_create(customer= user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item':0}
        cartItems = order['get_cart_item']
        
      
    return render(request, 'shop/index.html',
    { 
        'products': products,
        'cartItems': cartItems,
        'category' : cat,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'shop/index.html',{
                'message': 'Wrong login credentials'
            })
        
    return render(request,'shop/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        items : [] 
        
    return render(request, 'shop/cart.html',
    {
        'items' : items,
        'order' : order,
        'cartItems': cartItems,
    })

def checkout_view(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        
        user = Customer.objects.get(pk=customer.id)
            

    return render(request, 'shop/checkout.html',
    {
        'user': user,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    })

def updateItem(request):
    data =  json.loads(request.body)
    productId = data['productId']
    action = data['action']

    user =  request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = user, complete = False)
    orderItem, created =  OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0: 
        orderItem.delete()

    print('productId:',productId)
    print('action:',action)
    return JsonResponse('Added item', safe=False)

def searchCategory(request, id):
    cat =  Category.objects.all()
    products = Product.objects.all().filter(product_cat=id)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

        return render(request, 'shop/index.html',{
            'category': cat,
            'products': products,
            'cartItems': cartItems,
        })
        
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}
        cartItems = order['get_cart_item']
        
        return render(request, 'shop/index.html',{
            'category': cat,
            'products': products,
            'cartItems': cartItems,
        })
