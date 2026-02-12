from rest_framework import serializers
from .models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    На вход принимаем time_slot (id).
    user берём из request.user.
    """
    class Meta:
        model = Booking
        fields = ("id", "time_slot", "created_at")
        read_only_fields = ("id", "created_at")


class BookingListSerializer(serializers.ModelSerializer):
    """
    Для выдачи: показываем детали слота.
    """
    provider_name = serializers.CharField(source="time_slot.specialist.provider.name", read_only=True)
    specialist_name = serializers.SerializerMethodField()
    service_name = serializers.CharField(source="time_slot.service.name", read_only=True)
    start_time = serializers.DateTimeField(source="time_slot.start_time", read_only=True)
    end_time = serializers.DateTimeField(source="time_slot.end_time", read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "time_slot",
            "provider_name",
            "specialist_name",
            "service_name",
            "start_time",
            "end_time",
            "created_at",
        )

    def get_specialist_name(self, obj):
        first = obj.time_slot.specialist.first_name
        last = obj.time_slot.specialist.last_name or ""
        return f"{first} {last}".strip()
