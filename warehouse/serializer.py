from rest_framework import serializers

from .models import (
    Category, Unit, Product, Delivery, Order, OrderItem,
    Warehouse
)


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    unit = UnitSerializer()

    class Meta:
        model = Product
        fields = ["id", "barcode", "name", "category", "unit"]

#
# class DeliverySerializer(serializers.ModelSerializer):
#     product = ProductSerializer()
#     warehouse = serializers.StringRelatedField()
#     supplier = serializers.StringRelatedField()
#     responsible = serializers.StringRelatedField()
#
#     class Meta:
#         model = Delivery
#         fields = [
#             "id", "product", "warehouse", "supplier",
#             "quantity", "total_price", "delivery_date",
#             "responsible", "status"
#         ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price"]


# class OrderSerializer(serializers.ModelSerializer):
#     customer = serializers.StringRelatedField()
#     warehouse = serializers.StringRelatedField()
#     items = OrderItemSerializer(many=True)
#
#     class Meta:
#         model = Order
#         fields = ["id", "customer", "warehouse", "status", "order_date", "items"]
