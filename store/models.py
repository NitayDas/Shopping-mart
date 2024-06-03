
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