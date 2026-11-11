
from django.urls import path
from .views import menu_page, inventory_page

urlpatterns = [
    path("", menu_page, name="menu"),
    path("inventory/", inventory_page, name="inventory"),
]
