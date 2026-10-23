from django.contrib import admin
from .models import (
    Ingredient, StockItem, Recipe, StockMovement
)

admin.site.register(Ingredient)
admin.site.register(StockItem)
admin.site.register(Recipe)
admin.site.register(StockMovement)