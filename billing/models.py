
from django.db import models
from django.core.validators import MinValueValidator
from orders.models import Order


class Bill(models.Model):
    class Status(models.TextChoices):
        UNPAID = "UNPAID", "Unpaid"
        PARTIALLY_PAID = "PARTIALLY_PAID", "Partially Paid"
        PAID = "PAID", "Paid"
        VOID = "VOID", "Voided"

    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="bill",
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.UNPAID,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill #{self.pk} - Order #{self.order_id}"


class BillSplit(models.Model):
    class SplitType(models.TextChoices):
        EQUAL = "EQUAL", "Equal Split"
        BY_ITEM = "BY_ITEM", "By Item"
        BY_PERSON = "BY_PERSON", "By Person"

    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name="splits",
    )

    split_type = models.CharField(
        max_length=10,
        choices=SplitType.choices,
    )

    label = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: Person 1 or Guest A",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return f"{self.bill} - {self.label or self.split_type}"


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = "CASH", "Cash"
        CARD = "CARD", "Card"
        UPI = "UPI", "UPI / QR"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    bill = models.ForeignKey(
        Bill,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    split = models.ForeignKey(
        BillSplit,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="payments",
    )

    method = models.CharField(
        max_length=10,
        choices=Method.choices,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
    )

    reference = models.CharField(
        max_length=150,
        blank=True,
        help_text="Payment or transaction reference",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.pk} - {self.method}"
