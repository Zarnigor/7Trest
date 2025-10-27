from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WarehouseListCreateView, WarehouseDetailView,
    ReportAPIView, StockReportAPIView, DashboardReportView, CategoryViewSet, UnitViewSet,
    ProductViewSet, ProductPriceViewSet
)

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("units", UnitViewSet)
router.register("products", ProductViewSet)

urlpatterns = [
    path("warehouses/", WarehouseListCreateView.as_view(), name="warehouse-list-create"),
    path("warehouses/<int:pk>/", WarehouseDetailView.as_view(), name="warehouse-detail"),

    # path("dashboard/<int:warehouse_id>/", DashboardReportView.as_view(), name="warehouse-dashboard"),
    # path("report/", ReportAPIView.as_view(), name="report"),
    # path("reports/stock/", StockReportAPIView.as_view(), name="stock_report_api"),

    path("", include(router.urls)),
]
