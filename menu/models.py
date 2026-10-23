
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    class Station(models.TextChoices):
        KITCHEN = "KITCHEN", "Kitchen"
        BAR = "BAR", "Bar"
        COFFEE = "COFFEE", "Coffee Station"

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="menu_items",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    station = models.CharField(
        max_length=10,
        choices=Station.choices,
        default=Station.KITCHEN,
    )

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_menu_item_per_category",
            ),
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="menu_item_price_nonnegative",
            ),
            models.CheckConstraint(
                condition=models.Q(cost_price__gte=0),
                name="menu_item_cost_nonnegative",
            ),
        ]

    def __str__(self):
        return self.name


class Modifier(models.Model):
    name = models.CharField(max_length=100)
    additional_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    menu_items = models.ManyToManyField(
        MenuItem,
        related_name="modifiers",
        blank=True,
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Combo(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    items = models.ManyToManyField(
        MenuItem,
        through="ComboItem",
        related_name="combos",
    )
    combo_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ComboItem(models.Model):
    combo = models.ForeignKey(
        Combo,
        on_delete=models.CASCADE,
        related_name="combo_items",
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["combo", "menu_item"],
                name="unique_item_per_combo",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="combo_item_quantity_positive",
            ),
        ]

    def __str__(self):
        return f"{self.combo.name} - {self.menu_item.name}"


class HappyHourRule(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = "PERCENT", "Percentage"
        FIXED = "FIXED", "Fixed amount off"

    name = models.CharField(max_length=100)

    start_time = models.TimeField()
    end_time = models.TimeField()

    # Weekday numbers: Monday=0 through Sunday=6.
    weekdays = models.JSONField(default=list)

    discount_type = models.CharField(
        max_length=10,
        choices=DiscountType.choices,
        default=DiscountType.PERCENT,
    )
    discount_value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    menu_items = models.ManyToManyField(
        MenuItem,
        related_name="happy_hour_rules",
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
