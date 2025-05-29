from django.shortcuts import render,redirect,get_object_or_404
from store.models import *
from .forms import ProductForm
from django.views.generic import ListView
from django.db.models import F

def Admin_view(request):
    products = Product.objects.all()
    context={
        'products':products,
    }
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        discount = request.POST.get('discount')
        digital = request.POST.get('digital') == 'on'  # Checkbox value
        image = request.FILES.get('image')
        
        # Calculate discount price
        discount_price = float(price) - (float(price) * (float(discount) / 100))
        
        # Create and save the new Product instance
        new_product = Product(
            name=name,
            price=price,
            quantity=quantity,
            discount=discount,
            discount_price=discount_price,
            digital=digital,
            image=image
        )
        new_product.save()
        
        return redirect('admin_view')
    
    return render(request, 'admin/admin_page.html',context)




def update_product(request,id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        discount = request.POST.get('discount')
        digital = request.POST.get('digital') == 'on' 
        image = request.FILES.get('image')
        
        product.name = name
        product.price = price
        product.quantity = quantity
        product.discount = discount
        product.discount_price = float(price) - (float(price) * (float(discount) / 100))
        product.digital = digital
        
        if image:
            product.image = image
        
        product.save()
        return redirect('admin_view')
    
    return render(request, 'admin/update_product.html',{'product': product})


def delete_product(request,id):
    product= Product.objects.get(id=id)
    product.delete()
    return redirect('admin_view')


def Refund_List(request):
    
    user = request.user
    user_is_admin=False
   
    if user.is_staff:
        # Admin view
        user_is_admin= True
        refund_requests = Refund.objects.all().order_by('date_requested')
        item_refund_requests = refundItem.objects.all().order_by('-date_requested')
    else:
        # User view
        customer = user.customer
        orders = Order.objects.filter(customer=customer)
        refund_requests = Refund.objects.filter(order__in=orders).order_by('date_requested')
        item_refund_requests = refundItem.objects.filter(order__in=orders).order_by('-date_requested')

    context = {
        'refund_requests': refund_requests,
        'item_refund_requests': item_refund_requests,
        'user_is_admin':user_is_admin
     }

    return render(request, 'admin/refund_lists.html', context)



def approve_request(request, refun_id):
    refund_request = Refund.objects.get(id=refun_id)
    refund_request.status = 'approved'
    refund_request.save()
    
    order = refund_request.order
    order.refund_granted = True
    order.save()

   
    order_items = refund_request.order.orderitem_set.all()

    # Update the quantity of the corresponding product in the database
    for item in order_items:
        Product.objects.filter(id=item.product.id).update(quantity=F('quantity') + item.quantity)
        
        free_item = item.get_free_item
        free_item_quantity = item.get_free_item_quantity
        if free_item:
            free_item.quantity += free_item_quantity
            free_item.save()
        
        item.free_items = free_item_quantity
        item.save()

    
    return redirect('refund_lists')


def item_approve_request(request, refun_id):
    refund_request = refundItem.objects.get(id=refun_id)
    refund_request.status = 'approved'
    refund_request.save()
    
    order = refund_request.order
    product = refund_request.item
    
    #decrease the orderitem quantity
    item = order.orderitem_set.get(product=product)
    free_item_before = item.free_items
    item.quantity -= refund_request.quantity
    item.save()
    
    # get the current free items user should have
    free_item = item.get_free_item
    free_item_quantity_now = item.get_free_item_quantity
    
    # returned free items
    free_item_quantity = free_item_before - free_item_quantity_now
    if free_item:
        free_item.quantity += free_item_quantity
        free_item.save()
    
    # set item free items
    item.free_items = free_item_quantity_now
    item.save()
    
    # Update the quantity of the corresponding product in the database
    product.quantity += refund_request.quantity 
    product.save()
    
    return redirect('refund_lists')
    