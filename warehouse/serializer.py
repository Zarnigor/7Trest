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

from rest_framework import serializers
from .models import User, Role, Warehouse, UserWarehouse


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "description"]


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source="role", write_only=True
    )
    warehouses = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), many=True, write_only=True
    )
    warehouse_list = WarehouseSerializer(source="userwarehouse_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "full_name", "email", "phone", "password_hash",
            "role", "role_id", "warehouses", "warehouse_list",
            "is_active", "created_at"
        ]
        extra_kwargs = {"password_hash": {"write_only": True}}

    def create(self, validated_data):
        warehouses = validated_data.pop("warehouses", [])
        user = User.objects.create(**validated_data)
        for wh in warehouses:
            UserWarehouse.objects.create(user=user, warehouse=wh)
        return user
