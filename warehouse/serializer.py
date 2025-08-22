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

class StockReportSerializer(serializers.Serializer):
    barcode = serializers.CharField()
    name = serializers.CharField()
    unit = serializers.CharField()
    inbound_qty = serializers.DecimalField(max_digits=12, decimal_places=2)
    inbound_val = serializers.DecimalField(max_digits=15, decimal_places=2)
    outbound_qty = serializers.DecimalField(max_digits=12, decimal_places=2)
    outbound_val = serializers.DecimalField(max_digits=15, decimal_places=2)
    balance_qty = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance_val = serializers.DecimalField(max_digits=15, decimal_places=2)


from rest_framework import serializers


class VPutyReportSerializer(serializers.Serializer):
    summa = serializers.DecimalField(max_digits=15, decimal_places=2)
    kg = serializers.DecimalField(max_digits=15, decimal_places=2)
    ltr = serializers.DecimalField(max_digits=15, decimal_places=2)
    metr = serializers.DecimalField(max_digits=15, decimal_places=2)


class DostavlenReportSerializer(serializers.Serializer):
    summa = serializers.DecimalField(max_digits=15, decimal_places=2)
    kg = serializers.DecimalField(max_digits=15, decimal_places=2)
    ltr = serializers.DecimalField(max_digits=15, decimal_places=2)
    metr = serializers.DecimalField(max_digits=15, decimal_places=2)


class NaSkladeReportSerializer(serializers.Serializer):
    kolichestvo = serializers.DecimalField(max_digits=15, decimal_places=2)
    vernulsya = serializers.DecimalField(max_digits=15, decimal_places=2)
    tsena = serializers.DecimalField(max_digits=15, decimal_places=2)


class DashboardReportSerializer(serializers.Serializer):
    v_puti = VPutyReportSerializer()
    dostavlen = DostavlenReportSerializer()
    na_sklade = NaSkladeReportSerializer()
