from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('warehouse.urls')),
    path('api/', include('users.urls')),
    path('api/', include('product.urls')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),  # raw schema (YAML/JSON)
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),  # Swagger UI
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),  # ReDoc UI
]
 