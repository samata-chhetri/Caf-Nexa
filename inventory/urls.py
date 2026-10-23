from django.urls import path
from core.views import inventory_page

urlpatterns = [
    path("", inventory_page, name="inventory"),
]