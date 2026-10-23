from django.contrib import admin
from .models import (
    Category, MenuItem, Modifier,
    Combo, ComboItem, HappyHourRule
)

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Modifier)
admin.site.register(Combo)
admin.site.register(ComboItem)
admin.site.register(HappyHourRule)