from django.urls import path
from core.views import kitchen_page

urlpatterns = [
    path("", kitchen_page, name="kitchen"),
]