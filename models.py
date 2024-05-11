from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    description = models.TextField()
    specifications = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    supplier = models.CharField(max_length=255)
    delivery_method = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    def id(self):
        return self.Category.category

    id.short_description = "Category ID"
    id.admin_order_field = "category__category"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', null= True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.user.username}'s cart"

    def total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=30)
    card_name = models.CharField(max_length=30)
    card_id = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    method_delivery = models.CharField(max_length=255)
    bonus_cod = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.date}"


