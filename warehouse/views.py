from django.db.models import Sum
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Delivery, Category
from .models import Warehouse, StockMovement
from .serializer import WarehouseSerializer


class WarehouseListView(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer



# class DashboardView(generics.RetrieveAPIView):
#     def get(self, request, warehouse_id):
#         warehouse = Warehouse.objects.get(id=warehouse_id)
#
#         in_transit = StockMovement.objects.filter(
#             warehouse=warehouse, movement_type="inbound"
#         ).aggregate(
#             qty=Sum("quantity"), value=Sum("total_value")
#         )
#
#         delivered = StockMovement.objects.filter(
#             warehouse=warehouse, movement_type="outbound"
#         ).aggregate(
#             qty=Sum("quantity"), value=Sum("total_value")
#         )
#
#         in_stock = StockMovement.objects.filter(
#             warehouse=warehouse
#         ).aggregate(
#             qty=Sum("quantity"), value=Sum("total_value")
#         )
#
#         return Response({
#             "warehouse": warehouse.name,
#             "in_transit": {"quantity": in_transit["qty"] or 0, "value": in_transit["value"] or 0},
#             "delivered": {"quantity": delivered["qty"] or 0, "value": delivered["value"] or 0},
#             "in_stock": {
#                 "quantity": in_stock["qty"] or 0,
#                 "returned": 20000,   # agar return system qo‘shilgan bo‘lsa, alohida hisoblanadi
#                 "value": in_stock["value"] or 0
#             }
#         })


# class ShipmentReportView(generics.ListAPIView):
#     def get(self, request):
#         warehouse_id = request.query_params.get("warehouse_id")
#         date_from = request.query_params.get("date_from")
#         date_to = request.query_params.get("date_to")
#
#         warehouse = Warehouse.objects.get(id=warehouse_id)
#         categories = Category.objects.all()
#
#         data = []
#         for cat in categories:
#             products = Product.objects.filter(category=cat)
#             product_data = []
#             for p in products:
#                 movements = StockMovement.objects.filter(
#                     product=p, warehouse=warehouse,
#                     movement_type="outbound",
#                     created_at__date__range=[date_from, date_to]
#                 ).aggregate(
#                     qty=Sum("quantity"), value=Sum("total_value")
#                 )
#                 if movements["qty"]:
#                     product_data.append({
#                         "product": p.name,
#                         "unit": p.unit.abbreviation,
#                         "shipped_qty": movements["qty"],
#                         "shipped_value": movements["value"]
#                     })
#
#             if product_data:
#                 data.append({"name": cat.name, "products": product_data})
#
#         return Response({
#             "warehouse": warehouse.name,
#             "date_from": date_from,
#             "date_to": date_to,
#             "categories": data
#         })


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
