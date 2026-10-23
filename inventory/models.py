
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    name = models.CharField(max_length=150, unique=True)
    unit = models.CharField(
        max_length=20,
        help_text="Examples: g, ml, kg, litre",
    )
    current_stock = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0,
    )
    reorder_level = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0,
    )
    cost_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.current_stock <= self.reorder_level


class StockItem(models.Model):
    class Category(models.TextChoices):
        FOOD = "FOOD", "Food"
        BEVERAGE = "BEVERAGE", "Beverage"
        LIQUOR = "LIQUOR", "Liquor"
        OTHER = "OTHER", "Other"

    name = models.CharField(max_length=150, unique=True)

    category = models.CharField(
        max_length=10,
        choices=Category.choices,
    )

    unit = models.CharField(
        max_length=20,
        help_text="Examples: bottle, can, packet, litre",
    )

    current_stock = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0,
    )

    reorder_level = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0,
    )

    cost_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.current_stock <= self.reorder_level


class Recipe(models.Model):
    menu_item = models.ForeignKey(
        "menu.MenuItem",
        on_delete=models.CASCADE,
        related_name="recipes",
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name="recipes",
    )

    quantity_required = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(0.001)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["menu_item", "ingredient"],
                name="unique_ingredient_per_recipe",
            ),
        ]

    def __str__(self):
        return f"{self.menu_item.name} - {self.ingredient.name}"


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        PURCHASE = "PURCHASE", "Purchase"
        SALE = "SALE", "Consumption or Sale"
        WASTAGE = "WASTAGE", "Wastage"
        ADJUSTMENT = "ADJUSTMENT", "Adjustment"
        RETURN = "RETURN", "Return"

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="movements",
    )

    stock_item = models.ForeignKey(
        StockItem,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="movements",
    )

    movement_type = models.CharField(
        max_length=12,
        choices=MovementType.choices,
    )

    # Positive for stock added, negative for stock removed.
    quantity_change = models.DecimalField(
        max_digits=12,
        decimal_places=3,
    )

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        item = self.ingredient or self.stock_item
        return f"{item} - {self.movement_type}"
