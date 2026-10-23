from django.contrib import admin
from .models import (
    Order, OrderItem, OrderItemModifier, KitchenTicket
)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemModifier)
admin.site.register(KitchenTicket)