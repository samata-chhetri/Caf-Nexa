from django.urls import path
from core.views import reports_page

urlpatterns = [
    path("", reports_page, name="reports"),
]