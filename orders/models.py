
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

from core.models import RestaurantTable
from menu.models import MenuItem, Modifier


class Order(models.Model):
    class Source(models.TextChoices):
        DINE_IN = "DINE_IN", "Dine-in"
        TAKEAWAY = "TAKEAWAY", "Takeaway"
        ZOMATO = "ZOMATO", "Zomato"
        SWIGGY = "SWIGGY", "Swiggy"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PREPARING = "PREPARING", "Preparing"
        READY = "READY", "Ready"
        SERVED = "SERVED", "Served"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    table = models.ForeignKey(
        RestaurantTable,
        on_delete=models.PROTECT,
        related_name="orders",
        null=True,
        blank=True,
    )

    source = models.CharField(
        max_length=10,
        choices=Source.choices,
        default=Source.DINE_IN,
    )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="restaurant_orders",
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PREPARING = "PREPARING", "Preparing"
        READY = "READY", "Ready"
        SERVED = "SERVED", "Served"
        CANCELLED = "CANCELLED", "Cancelled"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    # Snapshot of the selling price when the item is ordered.
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

    @property
    def line_total(self):
        return self.unit_price * self.quantity


class OrderItemModifier(models.Model):
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="selected_modifiers",
    )

    modifier = models.ForeignKey(
        Modifier,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField(default=1)

    # Preserve the add-on price at the time of ordering.
    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return f"{self.modifier.name} for {self.order_item}"


class KitchenTicket(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        PREPARING = "PREPARING", "Preparing"
        READY = "READY", "Ready"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="kitchen_tickets",
    )

    station = models.CharField(
        max_length=10,
        choices=[
            ("KITCHEN", "Kitchen"),
            ("BAR", "Bar"),
            ("COFFEE", "Coffee Station"),
        ],
    )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.NEW,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KOT #{self.pk} - Order #{self.order_id}"
