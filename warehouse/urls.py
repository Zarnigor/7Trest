from django.urls import path
from .views import WarehouseListView, ReportAPIView, StockReportAPIView, DashboardReportView, RoleListView, UserListCreateView, UserDetailView

urlpatterns = [
    path("warehouses/", WarehouseListView.as_view(), name="warehouse-list"),
    path("dashboard/<int:warehouse_id>/", DashboardReportView.as_view(), name="warehouse-dashboard"),
    # path("reports/shipments/", ShipmentReportView.as_view(), name="shipment-report"),
    path("report/", ReportAPIView.as_view(), name="report"),
    path("reports/stock/", StockReportAPIView.as_view(), name="stock_report_api"),
    path("warehouses/", WarehouseListView.as_view(), name="warehouse-list"),
    path("roles/", RoleListView.as_view(), name="role-list"),
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<uuid:pk>/", UserDetailView.as_view(), name="user-detail"),
]
