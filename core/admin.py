from django.contrib import admin
from .models import RestaurantTable


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = (
        "table_number",
        "capacity",
        "status",
        "is_active",
    )

    list_filter = ("status", "is_active")
    search_fields = ("table_number",)
    ordering = ("table_number",)