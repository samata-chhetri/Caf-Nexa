
from django.db import models
from orders.models import Order


class ExternalOrder(models.Model):
    class Platform(models.TextChoices):
        ZOMATO = "ZOMATO", "Zomato"
        SWIGGY = "SWIGGY", "Swiggy"

    class SyncStatus(models.TextChoices):
        RECEIVED = "RECEIVED", "Received"
        IMPORTED = "IMPORTED", "Imported"
        FAILED = "FAILED", "Failed"

    platform = models.CharField(
        max_length=10,
        choices=Platform.choices,
    )

    external_order_id = models.CharField(max_length=150)

    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="external_order",
    )

    sync_status = models.CharField(
        max_length=10,
        choices=SyncStatus.choices,
        default=SyncStatus.RECEIVED,
    )

    # Store the received payload for troubleshooting.
    raw_payload = models.JSONField(default=dict, blank=True)

    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["platform", "external_order_id"],
                name="unique_external_order_per_platform",
            ),
        ]

    def __str__(self):
        return f"{self.platform} - {self.external_order_id}"


class IntegrationLog(models.Model):
    class Level(models.TextChoices):
        INFO = "INFO", "Info"
        WARNING = "WARNING", "Warning"
        ERROR = "ERROR", "Error"

    platform = models.CharField(
        max_length=10,
        choices=ExternalOrder.Platform.choices,
    )

    level = models.CharField(
        max_length=10,
        choices=Level.choices,
        default=Level.INFO,
    )

    message = models.TextField()
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} - {self.level} - {self.created_at}"
