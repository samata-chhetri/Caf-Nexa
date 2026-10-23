
from django.urls import path
from . import views

urlpatterns = [
    path("", views.table_management, name="table_management"),
]
