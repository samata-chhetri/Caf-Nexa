

from django.shortcuts import render
from django.db.models import F

from .models import Category, MenuItem, InventoryItem


def menu_page(request):
    categories = Category.objects.all().order_by("name")

    items = (
        MenuItem.objects
        .filter(is_available=True)
        .select_related("category")
        .order_by("category__name", "name")
    )

    return render(
        request,
        "menu/menu_page.html",
        {
            "categories": categories,
            "items": items,
        },
    )


def inventory_page(request):

    inventory_items = InventoryItem.objects.filter(
        is_active=True
    ).order_by("name")

    total_items = inventory_items.count()

    out_of_stock = inventory_items.filter(
        quantity__lte=0
    ).count()

    low_stock = inventory_items.filter(
        quantity__gt=0,
        quantity__lte=F("minimum_stock")
    ).count()

    available_stock = inventory_items.filter(
        quantity__gt=F("minimum_stock")
    ).count()

    context = {
        "inventory_items": inventory_items,
        "total_items": total_items,
        "available_stock": available_stock,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
    }

    return render(
        request,
        "menu/inventory.html",
        context
    )
