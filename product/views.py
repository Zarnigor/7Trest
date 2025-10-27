from rest_framework import viewsets
from .models import Category, Unit, Product, ProductPrice
from .serializers import CategorySerializer, UnitSerializer, ProductSerializer, ProductPriceSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related("category", "unit")
    serializer_class = ProductSerializer


class ProductPriceViewSet(viewsets.ModelViewSet):
    queryset = ProductPrice.objects.all().select_related("product")
    serializer_class = ProductPriceSerializer
