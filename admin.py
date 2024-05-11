from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "specifications", "price", "stock", "supplier", "delivery_method", "category"]
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user

        return queryset

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user

        return queryset

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user

        return queryset

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'address', 'card_name', 'card_id', 'expiration_date', 'method_delivery', 'bonus_cod']
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user

        return queryset
