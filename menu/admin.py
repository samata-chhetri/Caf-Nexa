
from django.contrib import admin

from .models import (
    Category,
    MenuItem,
    Modifier,
    Combo,
    ComboItem,
    HappyHourRule,
    InventoryItem,
)


admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Modifier)
admin.site.register(Combo)
admin.site.register(ComboItem)
admin.site.register(HappyHourRule)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'quantity',
        'unit',
        'minimum_stock',
        'purchase_price',
        'supplier',
        'stock_status',
        'is_active',
    )

    list_filter = ('category', 'unit', 'is_active')

    search_fields = ('name', 'category', 'supplier')

    list_editable = ('quantity', 'minimum_stock', 'is_active')

    ordering = ('name',)
