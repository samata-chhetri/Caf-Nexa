
from django.shortcuts import render
from .models import RestaurantTable


def table_management(request):
    tables = RestaurantTable.objects.filter(
        is_active=True
    ).order_by("table_number")

    return render(
        request,
        "core/tables.html",
        {"tables": tables},
    )

def dashboard(request):
    context = {
        "total_tables": 12,
        "available_tables": 8,
        "occupied_tables": 3,
        "bill_requested": 1,
        "today_sales": 12500,
        "active_orders": 4,
    }

    return render(request, "core/dashboard.html", context)


def module_placeholder(request, title, description):
    return render(
        request,
        "core/coming_soon.html",
        {
            "page_title": title,
            "description": description,
        },
    )


def menu_page(request):
    return module_placeholder(
        request,
        "Menu & Orders",
        "Manage menu items, modifiers, combos and restaurant orders.",
    )


def kitchen_page(request):
    return module_placeholder(
        request,
        "Kitchen Tickets",
        "View and manage food, bar and coffee preparation tickets.",
    )


def inventory_page(request):
    return module_placeholder(
        request,
        "Inventory",
        "Manage ingredients, beverages, liquor and stock alerts.",
    )


def billing_page(request):
    return module_placeholder(
        request,
        "Billing & Payments",
        "Generate bills, split payments and record payment methods.",
    )


def reports_page(request):
    return module_placeholder(
        request,
        "Analytics",
        "View restaurant sales, category revenue and profit reports.",
    )
