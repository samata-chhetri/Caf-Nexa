from django.urls import path
from core.views import menu_page

urlpatterns = [
    path("", menu_page, name="menu"),
]