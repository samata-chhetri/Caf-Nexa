from django.urls import path
from core.views import billing_page

urlpatterns = [
    path("", billing_page, name="billing"),
]