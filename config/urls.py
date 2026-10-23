
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("tables/", include("core.table_urls")),
    path("menu/", include("menu.urls")),
    path("kitchen/", include("orders.kitchen_urls")),
    path("inventory/", include("inventory.urls")),
    path("billing/", include("billing.urls")),
    path("reports/", include("reports.urls")),
]
