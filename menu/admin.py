
from django.contrib import admin
from .models import (
    Category,
    MenuItem,
    Modifier,
    Combo,
    ComboItem,
    HappyHourRule,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "station",
        "is_available",
    )

    list_filter = ("category", "station", "is_available")
    search_fields = ("name", "category__name")
    list_editable = ("price", "is_available")


@admin.register(Modifier)
class ModifierAdmin(admin.ModelAdmin):
    list_display = ("name", "additional_price", "is_available")
    list_filter = ("is_available",)
    search_fields = ("name",)


@admin.register(Combo)
class ComboAdmin(admin.ModelAdmin):
    list_display = ("name", "combo_price", "is_available")
    list_filter = ("is_available",)
    search_fields = ("name",)


@admin.register(ComboItem)
class ComboItemAdmin(admin.ModelAdmin):
    list_display = ("combo", "menu_item", "quantity")
    list_filter = ("combo",)


@admin.register(HappyHourRule)
class HappyHourRuleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_time",
        "end_time",
        "is_active",
    )
    list_filter = ("is_active", "discount_type")
    search_fields = ("name",)
