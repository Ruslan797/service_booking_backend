# from rest_framework import serializers
# from .models import Service, Provider, TimeSlot
#
#
# class ProviderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Provider
#         fields = ("id", "name", "is_active")
#
#
# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = ("id", "name", "description", "duration_minutes", "price", "is_active")
#
#
# class TimeSlotSerializer(serializers.ModelSerializer):
#     provider_name = serializers.CharField(source="specialist.provider.name", read_only=True)
#     specialist_name = serializers.SerializerMethodField()
#     service_name = serializers.CharField(source="service.name", read_only=True)
#
#     class Meta:
#         model = TimeSlot
#         fields = (
#             "id",
#             "provider_name",
#             "specialist_name",
#             "service_name",
#             "start_time",
#             "end_time",
#             "is_booked",
#         )
#
#     def get_specialist_name(self, obj):
#         # чтобы было красиво даже если last_name пустой
#         return f"{obj.specialist.first_name} {obj.specialist.last_name}".strip()


from rest_framework import serializers
from .models import Provider, Specialist, Service, TimeSlot


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ("id", "name", "is_active")


class SpecialistSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source="provider.name", read_only=True)

    class Meta:
        model = Specialist
        fields = ("id", "provider", "provider_name", "first_name", "last_name", "is_active")


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "name", "description", "duration_minutes", "price", "is_active")


class TimeSlotSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source="specialist.provider.name", read_only=True)
    specialist_name = serializers.SerializerMethodField()
    service_name = serializers.CharField(source="service.name", read_only=True)

    class Meta:
        model = TimeSlot
        fields = (
            "id",
            "specialist",
            "specialist_name",
            "provider_name",
            "service",
            "service_name",
            "start_time",
            "end_time",
            "is_booked",
        )

    def get_specialist_name(self, obj):
        return f"{obj.specialist.first_name} {obj.specialist.last_name}".strip()


