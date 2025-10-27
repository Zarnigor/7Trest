from django.db import models
import uuid
from django.contrib.auth.hashers import make_password, check_password

class Warehouse(models.Model):
    WAREHOUSE_TYPES = [
        ("central", "Central"),
        ("regional", "Regional"),
        ("store", "Store"),
    ]

    name = models.CharField(max_length=100)
    location = models.TextField()
    type = models.CharField(max_length=50, choices=WAREHOUSE_TYPES, default='regional')
    capacity = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # tonna/litr/kubm
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



# ========================
# Products & Categories
# ========================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)  # kg, litr, dona
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.abbreviation


class Product(models.Model):
    barcode = models.CharField(max_length=100, unique=True)  # endi string
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    quantity_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # masalan: 25.00 (25kg)
    stock_quantity = models.PositiveIntegerField(default=0)  # nechta 25kg qop bor
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.quantity_per_unit} {self.unit})"


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


# ========================
# Suppliers & Customers
# ========================
class Supplier(models.Model):
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# ========================
# Deliveries (Inbound)
# ========================
class Delivery(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    delivery_date = models.DateField()
    # responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ========================
# Orders (Outbound)
# ========================
class Order(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    order_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)


# ========================
# Stock Movements
# ========================
class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ("inbound", "Inbound"),
        ("outbound", "Outbound"),
        ("return", "Return"),
        ("transfer", "Transfer"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    reference_id = models.IntegerField(null=True, blank=True)  # delivery_id yoki order_id
    created_at = models.DateTimeField(auto_now_add=True)


# ========================
# Inventory & Audits
# ========================
class InventoryCheck(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    counted_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    check_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
