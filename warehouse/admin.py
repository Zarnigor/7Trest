# warehouse/admin.py

from django.contrib import admin
from .models import Product, Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'capacity')
    search_fields = ('name', 'location')
    list_filter = ('location',)
    ordering = ('id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass