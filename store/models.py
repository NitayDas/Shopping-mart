from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(max_length=200, null=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    quantity = models.IntegerField(default=10)
    discount = models.FloatField(max_length=100,default=0,null=True)
    discount_price =models.FloatField(max_length=100,default=0,null=True)
    bulk_discount_threshold = models.IntegerField(default=0, null=True, blank=True)
    bulk_discount_free_items = models.IntegerField(default=0, null=True, blank=True)
    free_item_for = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='free_item')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('not_ordered', 'Not Ordered'),
        ('complete', 'Complete'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='not_ordered')
    # transaction_id = models.CharField(max_length=200, null=True)
    refund_requested = models.BooleanField(null=True,default=False)
    refund_granted = models.BooleanField(null=True,default=False)
    

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping_cost(self):
        return int((self.get_cart_items + 4) / 5) * 5

    @property
    def total_with_shipping(self):
        return self.with_discount_get_cart_total + self.shipping_cost

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        print(shipping)
        return shipping


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def with_discount_get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.with_discount_get_total for item in orderitems])
        return total
            

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    free_items = models.IntegerField(default=0)
    

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    @property
    def with_discount_get_total(self):
        total=0.0
        if self.product.discount_price:
            total = self.product.discount_price * self.quantity
        else:
            total =self.product.price * self.quantity
        return total
    
    
    @property
    def get_free_item_quantity(self):
        if (
            self.product.bulk_discount_threshold > 0
            and self.quantity >= self.product.bulk_discount_threshold
        ):
            
            return (
                self.quantity // self.product.bulk_discount_threshold * 
                self.product.bulk_discount_free_items
            )
             
        else:
            return 0
        
        
    @property
    def get_free_item(self):
        if self.product.free_item_for:
            return self.product.free_item_for
        return None
    


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class Refund(models.Model):
    RETURN_STATUS_CHOICES = [
        ('no_refund','No_refund'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default='no_refund')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Return {self.id} for OrderItem {self.order.id}'
    
class refundItem(models.Model):
    RETURN_STATUS_CHOICES = [
        ('no_refund','No_refund'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default='no_refund')
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    refund_amount = models.FloatField(max_length=200, null=True)
    
    @property
    def get_status(self):
        return self.status

    def __str__(self):
        return f'Returnitem {self.item} for OrderItem {self.order.id}'
    