from django.urls import path
from .views import WarehouseListView, ReportAPIView

urlpatterns = [
    path("warehouses/", WarehouseListView.as_view(), name="warehouse-list"),
    # path("dashboard/<int:warehouse_id>/", DashboardView.as_view(), name="warehouse-dashboard"),
    # path("reports/shipments/", ShipmentReportView.as_view(), name="shipment-report"),
    path("report/", ReportAPIView.as_view(), name="report"),
]
