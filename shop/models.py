from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

user = get_user_model()

class Customer(models.Model):
    user = models.OneToOneField(user, models.CASCADE)
    name = models.CharField(max_length=150, blank=True, null=True)
    mobile = models.CharField(max_length=16,blank=True,null=True)
    username = models.CharField(max_length=16, blank=True ,null=True)
    address = models.TextField(blank=True, null=True )

    def __str__(self):
        return self.user.email


# Signals




class Category(models.Model):
    title = models.CharField(max_length=150)
    details = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)


class Brand(models.Model):
    title = models.CharField(max_length=150)
    details = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='brand/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)


class Product(models.Model):
    title = models.CharField(max_length=160)
    image = models.ImageField(upload_to='products/')
    oldprice = models.PositiveIntegerField(blank=True, null=True)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    category = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    view = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product}---{self.view}"
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    complit = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    quantity = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cart}--{self.total}"


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=16)
    address = models.TextField()
    email = models.CharField(max_length=100)
    order_status = models.CharField(
        max_length=100, choices=ORDER_STATUS, default="Order Received")


class TrendingProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Slider(models.Model):
    name = models.CharField(max_length=150)
    details = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='slider/')
    url = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.TextField()
    date = models.DateField(auto_now_add=True)