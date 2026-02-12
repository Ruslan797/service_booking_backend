from django.contrib import admin
from .models import Provider, Service, Specialist, TimeSlot


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    search_fields = ("name",)


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "provider", "is_active")
    list_filter = ("provider", "is_active")
    search_fields = ("first_name", "last_name", "provider__name")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "duration_minutes", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("id", "specialist", "service", "start_time", "end_time", "is_booked")
    list_filter = ("is_booked", "service", "specialist__provider")
    search_fields = (
        "specialist__first_name",
        "specialist__last_name",
        "specialist__provider__name",
        "service__name",
    )

