
from django.shortcuts import render
from .models import RestaurantTable


def dashboard(request):
    return render(request, "core/dashboard.html")



def table_management(request):
    tables = RestaurantTable.objects.filter(
        is_active=True
    ).order_by("table_number")

    context = {
        "tables": tables,
        "total_tables": tables.count(),
        "available_tables": tables.filter(
            status=RestaurantTable.Status.AVAILABLE
        ).count(),
        "occupied_tables": tables.filter(
            status=RestaurantTable.Status.OCCUPIED
        ).count(),
        "bill_requested_tables": tables.filter(
            status=RestaurantTable.Status.BILL_REQUESTED
        ).count(),
    }

    return render(request, "core/tables.html", context)



def module_placeholder(
    request,
    title,
    description,
    active_page,
    section_title,
    section_description,
    section_icon,
    metrics,
    setup_message,
):
    context = {
        "title": title,
        "description": description,
        "active_page": active_page,
        "section_title": section_title,
        "section_description": section_description,
        "section_icon": section_icon,
        "metric_one_label": metrics[0][0],
        "metric_one_value": metrics[0][1],
        "metric_one_note": metrics[0][2],
        "metric_two_label": metrics[1][0],
        "metric_two_value": metrics[1][1],
        "metric_two_note": metrics[1][2],
        "metric_three_label": metrics[2][0],
        "metric_three_value": metrics[2][1],
        "metric_three_note": metrics[2][2],
        "setup_message": setup_message,
    }

    return render(
        request,
        "core/workspace_page.html",
        context,
    )


def menu_page(request):
    return module_placeholder(
        request, "Menu & Orders",
        "Manage your menu, pricing and restaurant orders.",
        "menu", "Menu management",
        "Quick access to your menu and order records.", "☷",
        [
            ("Menu categories", "—", "Data not connected"),
            ("Menu items", "—", "Data not connected"),
            ("Restaurant orders", "—", "Data not connected"),
        ],
        "Menu and order actions currently open Django Admin. "
        "The staff ordering workflow still needs implementation.",
    )


def kitchen_page(request):
    return module_placeholder(
        request, "Kitchen Tickets",
        "Organise kitchen preparation and order fulfilment.",
        "kitchen", "Kitchen operations",
        "Access recorded orders and kitchen tickets.", "♨",
        [
            ("Pending tickets", "—", "Live queue not connected"),
            ("Preparing", "—", "Live queue not connected"),
            ("Completed", "—", "Live queue not connected"),
        ],
        "Live kitchen updates and automatic KOT routing "
        "are not implemented yet.",
    )


def inventory_page(request):
    return module_placeholder(
        request, "Inventory",
        "Monitor ingredients, stock levels and supplies.",
        "inventory", "Stock management",
        "Manage inventory records from one workspace.", "▣",
        [
            ("Ingredients", "—", "Stock totals not connected"),
            ("Stock items", "—", "Stock totals not connected"),
            ("Low stock", "—", "Alerts not implemented"),
        ],
        "Stock deduction, low-stock alerts and inventory "
        "calculations still need to be connected.",
    )


def billing_page(request):
    return module_placeholder(
        request, "Billing & Payments",
        "Manage bills, payments and bill splits.",
        "billing", "Billing workspace",
        "Access saved billing and payment records.", "₹",
        [
            ("Bills", "—", "Totals not connected"),
            ("Payments", "—", "Payment totals not connected"),
            ("Bill splits", "—", "Split calculations not connected"),
        ],
        "Bill generation, split payments and payment "
        "processing still need implementation.",
    )


def reports_page(request):
    return module_placeholder(
        request, "Analytics",
        "Explore restaurant sales and operational performance.",
        "reports", "Performance overview",
        "Access records used to build restaurant reports.", "▥",
        [
            ("Revenue", "—", "Calculation not connected"),
            ("Top sellers", "—", "Calculation not connected"),
            ("Profit", "—", "Calculation not connected"),
        ],
        "Analytics will display real figures after sales, "
        "order and cost calculations are implemented.",
    )
