
from django.db import models


class RestaurantTable(models.Model):

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        OCCUPIED = "OCCUPIED", "Occupied"
        BILL_REQUESTED = "BILL_REQUESTED", "Bill Requested"

    table_number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(default=4)

    # Position for the visual floor plan
    position_x = models.PositiveIntegerField(default=0)
    position_y = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number}"
