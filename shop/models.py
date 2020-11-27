from django.db import models

from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length = 255, null=True, blank=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.name

class Category(models.Model):
    category_name =  models.CharField(max_length = 255, null = False, blank = False)

    def __str__(self):
        return self.category_name

class Specifications(models.Model):
    display = models.CharField(max_length = 255, blank =True, null=True)
    camera = models.CharField(max_length = 255, blank =True, null=True)
    memory = models.CharField(max_length = 255, blank =True, null=True)
    battery= models.CharField(max_length = 255, blank =True, null=True)
    warranty = models.CharField(max_length = 255, blank =True, null=True)

    def __str__(self):
        return self.display

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(
        upload_to='product_images/', null=True, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    description = models.CharField(max_length=255)
    Specifications = models.ForeignKey(Specifications, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    order_id = models.CharField(max_length = 255, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.getTotal for item in order_items])
        return total

    @property
    def get_cart_item(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null= True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.name
    
    @property
    def getTotal(self):
        total_price = self.product.price * self.quantity
        return total_price
        


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    address= models.CharField(max_length = 255,null = False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length = 255,null=True, blank = True)
    county = models.CharField(max_length = 255,null=True, blank = True)
    town = models.CharField(max_length = 255,null=True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.address