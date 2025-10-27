from django.urls import path
from .views import WarehouseListCreateView, WarehouseDetailView

urlpatterns = [
    path("warehouses/", WarehouseListCreateView.as_view(), name="warehouse-list-create"),
    path("warehouses/<int:pk>/", WarehouseDetailView.as_view(), name="warehouse-detail"),

    # path("dashboard/<int:warehouse_id>/", DashboardReportView.as_view(), name="warehouse-dashboard"),
    # path("report/", ReportAPIView.as_view(), name="report"),
    # path("reports/stock/", StockReportAPIView.as_view(), name="stock_report_api"),
]
