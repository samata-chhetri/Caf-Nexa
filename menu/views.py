
from django.shortcuts import render
from .models import Category, MenuItem


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
