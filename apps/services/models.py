# from django.db import models
# from django.conf import settings
#
#
# class Provider(models.Model):
#     """
#     Специалист, который оказывает услуги.
#     В MVP может быть один (например: 'Main Provider').
#     """
#
#     name = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#
#     services = models.ManyToManyField(
#         "Service",
#         related_name="providers",
#         blank=True,
#     )
#
#     def __str__(self):
#         return self.name
#
#
# class Service(models.Model):
#     """
#     Услуга, которую можно забронировать.
#     """
#
#     name = models.CharField(max_length=150)
#     description = models.TextField(blank=True)
#     duration_minutes = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name
#
#
# class TimeSlot(models.Model):
#     provider = models.ForeignKey(
#         Provider,
#         on_delete=models.CASCADE,
#         related_name="time_slots"
#     )
#     service = models.ForeignKey(
#         Service,
#         on_delete=models.CASCADE,
#         related_name="time_slots",
#         null=True,
#         blank=True
#     )
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     is_booked = models.BooleanField(default=False)
#
#     class Meta:
#         ordering = ("start_time",)
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["provider", "service", "start_time", "end_time"],
#                 name="unique_timeslot_per_provider_service"
#             )
#         ]
#
#     def __str__(self):
#         return f"{self.provider} | {self.service} | {self.start_time} - {self.end_time}"

from django.db import models


class Provider(models.Model):
    """
    Клиника / организация.
    """
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    """
    Услуга.
    """
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.duration_minutes} min)"


class Specialist(models.Model):
    """
    Специалист (врач/мастер), который работает в клинике (Provider).
    """
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="specialists",
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return f"{full_name} — {self.provider.name}"


class TimeSlot(models.Model):
    """
    Доступный интервал времени для записи.
    Слот принадлежит конкретному специалисту и конкретной услуге.
    """
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        related_name="time_slots",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="time_slots",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ("start_time",)
        unique_together = ("specialist", "service", "start_time", "end_time")

    def __str__(self):
        return (
            f"{self.specialist.provider} | {self.specialist} | {self.service} | "
            f"{self.start_time} - {self.end_time}"
        )


