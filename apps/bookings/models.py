from django.conf import settings
from django.db import models
from apps.services.models import TimeSlot


class Booking(models.Model):
    """
    Факт бронирования пользователем конкретного тайм-слота.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    time_slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name="booking",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Booking #{self.id} — {self.user} — {self.time_slot}"
