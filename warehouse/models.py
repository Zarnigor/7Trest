from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Warehouse(models.Model):
    class WarehouseType(models.TextChoices):
        MAIN = 'MAIN', 'Asosiy ombor'
        OBJECT = 'OBJECT', 'Obyekt ombor'
        SMALL = 'SMALL', 'Kichik ombor'

    name = models.CharField(max_length=255)
    address = models.TextField()
    type = models.CharField(
        max_length=10,
        choices=WarehouseType.choices
    )
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='warehouses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    class Unit(models.TextChoices):
        METER = "m", "Metr"
        SQUARE_METER = "m2", "Kvadrat metr"
        CUBIC_METER = "m3", "Kub metr"
        PIECE = "dona", "Dona"
        TON = "tonna", "Tonna"
        LITER = "litr", "Litr"

    class Currency(models.TextChoices):
        UZS = "UZS", "So‘m"
        USD = "USD", "AQSh dollari"
        EUR = "EUR", "Yevro"

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True, null=True)

    unit = models.CharField(max_length=10, choices=Unit.choices)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.UZS)

    stock_quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    min_stock_level = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
