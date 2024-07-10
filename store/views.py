from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .utils import cookieCart, cartData
import json


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']

    products = Product.objects.all()
    
    for product in products:
        if product.discount:
            product.discount_price = product.price - product.price * product.discount/100
            product.save()
            
    context = {'products': products,'cartItems':cartItems}
    return render(request, 'store/store.html', context)



def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username,password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('store') 
        else:
            return HttpResponse('Invalid Username or Password !')
    
    return render(request, 'authentication/login.html')

def logoutpage(request):
    logout(request)
    return redirect('store')

def signup(request):
     if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        
        if password1!=password2:
            return HttpResponse('Invalid confirm password !')
        else:
            user = User.objects.create_user(username, email, password1)
            customer = Customer.objects.create(user=user, name=username, email=email)
            customer.save()
            return redirect('login')
        
     return render(request,'authentication/signup.html')
 
 
def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def updateItem(request):
    
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('productId:',productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    
    order, created = Order.objects.get_or_create(customer = customer,  status='not_ordered')
    
    orderItem , created = OrderItem.objects.get_or_create(order= order, product = product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1 )
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)
