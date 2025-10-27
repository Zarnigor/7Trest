from rest_framework import serializers
from .models import Category, Unit, Product, ProductPrice
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, write_only=True)
    start_date = serializers.DateField(write_only=True)

    class Meta:
        model = Product
        fields = [
            "barcode",
            "name",
            "category",
            "unit",
            "quantity_per_unit",
            "stock_quantity",
            "price",
            "start_date",
        ]

    def create(self, validated_data):
        price = validated_data.pop('price')
        start_date = validated_data.pop('start_date')
        product = Product.objects.create(**validated_data)
        ProductPrice.objects.create(product=product, price=price, start_date=start_date)
        return product

class ProductPriceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductPrice
        fields = ["id", "product", "product_name", "price", "start_date", "end_date"]

