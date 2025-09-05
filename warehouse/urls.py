from django.urls import path
from .views import (
    WarehouseListCreateView, WarehouseDetailView,
    ReportAPIView, StockReportAPIView, DashboardReportView,
    RoleListView, UserListCreateView, UserDetailView, PinLoginView
)

urlpatterns = [
    # Warehouses CRUD
    path("warehouses/", WarehouseListCreateView.as_view(), name="warehouse-list-create"),
    path("warehouses/<int:pk>/", WarehouseDetailView.as_view(), name="warehouse-detail"),

    # Dashboard & Reports
    path("dashboard/<int:warehouse_id>/", DashboardReportView.as_view(), name="warehouse-dashboard"),
    path("report/", ReportAPIView.as_view(), name="report"),
    path("reports/stock/", StockReportAPIView.as_view(), name="stock_report_api"),

    # Roles & Users
    path("roles/", RoleListView.as_view(), name="role-list"),
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<uuid:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("auth/pin-login/", PinLoginView.as_view(), name="pin-login"),
]
