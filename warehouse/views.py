from django.db.models import Sum
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import StockMovement
from .models import Delivery, Warehouse
from .serializer import DashboardReportSerializer, WarehouseSerializer
from rest_framework import viewsets
from .models import Category, Unit, Product, ProductPrice
from .serializer import (
    CategorySerializer,
    UnitSerializer,
    ProductSerializer,
    ProductPriceSerializer
)

class StockReportAPIView(APIView):
    """
    Общий отчет по оставшимся товарам
    """

    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        queryset = StockMovement.objects.select_related("product__category", "product__unit")

        if start_date and end_date:
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])

        data = []
        categories = Category.objects.all()

        for category in categories:
            products = Product.objects.filter(category=category)

            if products.exists():
                items = []
                for i, product in enumerate(products, start=1):
                    prod_movements = queryset.filter(product=product)

                    inbound = prod_movements.filter(movement_type="inbound") \
                        .aggregate(qty=Sum("quantity"), val=Sum("total_value"))
                    outbound = prod_movements.filter(movement_type="outbound") \
                        .aggregate(qty=Sum("quantity"), val=Sum("total_value"))
                    return_mov = prod_movements.filter(movement_type="return") \
                        .aggregate(qty=Sum("quantity"), val=Sum("total_value"))

                    inbound_qty = inbound["qty"] or 0
                    inbound_val = inbound["val"] or 0
                    outbound_qty = outbound["qty"] or 0
                    outbound_val = outbound["val"] or 0
                    return_qty = return_mov["qty"] or 0
                    return_val = return_mov["val"] or 0

                    balance_qty = inbound_qty - outbound_qty + return_qty
                    balance_val = inbound_val - outbound_val + return_val

                    items.append({
                        "№": i,
                        "Штрих-код": product.barcode,
                        "Название товара": product.name,
                        "Единица измерения": product.unit.abbreviation if product.unit else "",
                        "Добавлено за год (кол-во)": float(inbound_qty),
                        "Добавлено за год (сумма)": float(inbound_val),
                        "Выдано со склада (кол-во)": float(outbound_qty),
                        "Выдано со склада (сумма)": float(outbound_val),
                        "Возврат (кол-во)": float(return_qty),
                        "Возврат (сумма)": float(return_val),
                        "Остаток на складе (кол-во)": float(balance_qty),
                        "Остаток на складе (сумма)": float(balance_val),
                    })

                data.append({
                    "Категория": category.name,
                    "items": items
                })

        return Response(data)


class ReportAPIView(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        queryset = Delivery.objects.select_related("product__category", "product__unit")

        if start_date and end_date:
            queryset = queryset.filter(delivery_date__range=[start_date, end_date])

        data = []
        categories = Category.objects.all()

        for category in categories:
            deliveries = queryset.filter(product__category=category)

            if deliveries.exists():
                items = []
                total_sum = 0

                for i, d in enumerate(deliveries, start=1):
                    item_sum = d.total_price
                    total_sum += item_sum

                    items.append({
                        "№": i,
                        "Наименование товара": d.product.name,
                        "Кол-во": float(d.quantity),
                        "Ед. изм.": d.product.unit.abbreviation if d.product.unit else "",
                        "Куда доставлено": d.warehouse.name,
                        "Дата доставки": d.delivery_date,
                        "Цена за ед.": float(d.total_price / d.quantity),
                        "Сумма": float(item_sum)
                    })

                data.append({
                    "category": category.name,
                    "items": items,
                    "total": total_sum
                })

        return Response(data)



class DashboardReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        warehouse_id = request.query_params.get("warehouse_id")

        # Filter faqat bir ombor bo‘yicha
        delivery_filter = {}
        stock_filter = {}
        if warehouse_id:
            delivery_filter["warehouse_id"] = warehouse_id
            stock_filter["warehouse_id"] = warehouse_id

        # В пути
        v_puti_qs = Delivery.objects.filter(status="pending", **delivery_filter)
        v_puti_summa = v_puti_qs.aggregate(Sum("total_price"))["total_price__sum"] or 0

        # Доставлен
        dostavlen_qs = Delivery.objects.filter(status="completed", **delivery_filter)
        dostavlen_summa = dostavlen_qs.aggregate(Sum("total_price"))["total_price__sum"] or 0

        # На складе
        inbound = StockMovement.objects.filter(movement_type="inbound", **stock_filter).aggregate(
            qty=Sum("quantity"), val=Sum("total_value")
        )
        outbound = StockMovement.objects.filter(movement_type="outbound", **stock_filter).aggregate(
            qty=Sum("quantity"), val=Sum("total_value")
        )
        returned = StockMovement.objects.filter(movement_type="return", **stock_filter).aggregate(
            qty=Sum("quantity")
        )

        kolichestvo = (inbound["qty"] or 0) - (outbound["qty"] or 0)
        tsena = (inbound["val"] or 0) - (outbound["val"] or 0)
        vernulsya = returned["qty"] or 0

        data = {
            "v_puti": {
                "summa": v_puti_summa,
                "kg": 0,
                "ltr": 0,
                "metr": 0,
            },
            "dostavlen": {
                "summa": dostavlen_summa,
                "kg": 0,
                "ltr": 0,
                "metr": 0,
            },
            "na_sklade": {
                "kolichestvo": kolichestvo,
                "vernulsya": vernulsya,
                "tsena": tsena,
            }
        }

        serializer = DashboardReportSerializer(data)
        return Response(serializer.data)

#
# class RoleListView(generics.ListAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer
#     permission_classes = [IsAuthenticated]
#


class WarehouseListCreateView(generics.ListCreateAPIView):
    """
    GET /warehouses/  -> ro'yxat
    POST /warehouses/ -> yaratish
    """
    queryset = Warehouse.objects.all().order_by("name")
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]


class WarehouseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /warehouses/<id>/      -> bitta ombor
    PUT/PATCH /warehouses/<id>/-> yangilash
    DELETE /warehouses/<id>/   -> o'chirish
    """
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]


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
