from datetime import datetime, timedelta, time

from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Service, TimeSlot
from .serializers import ServiceSerializer, TimeSlotSerializer


class ServiceListCreateView(generics.ListCreateAPIView):
    """
    GET: список услуг (доступно авторизованным)
    POST: создать услугу (только админ)
    """
    queryset = Service.objects.all().order_by("id")
    serializer_class = ServiceSerializer

    def get_permissions(self):
        # GET -> IsAuthenticated, POST -> IsAdminUser
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]


class TimeSlotListView(generics.ListAPIView):
    """
    Список всех таймслотов (для дебага/админа).
    GET /api/services/time-slots/
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        return (
            TimeSlot.objects
            .select_related("specialist", "specialist__provider", "service")
            .order_by("start_time")
        )


class AvailableSlotsView(APIView):
    """
    Свободные слоты для конкретной услуги на конкретную дату.

    Пример:
    GET /api/services/1/available/?date=2026-01-28
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, service_id: int):
        # 1) берём дату из query params
        date_str = request.query_params.get("date")
        if not date_str:
            return Response(
                {"detail": "Query param 'date' is required. Format: YYYY-MM-DD"},
                status=400,
            )

        # 2) парсим дату
        try:
            day = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"detail": "Invalid date format. Use YYYY-MM-DD"},
                status=400,
            )

        # 3) границы дня: [00:00, 24:00)
        start_dt = timezone.make_aware(datetime.combine(day, time.min))
        end_dt = start_dt + timedelta(days=1)

        # 4) фильтруем: нужная услуга + нужный день + только свободные
        slots = (
            TimeSlot.objects
            .filter(
                service_id=service_id,
                start_time__gte=start_dt,
                start_time__lt=end_dt,
                is_booked=False,
            )
            .select_related("specialist", "specialist__provider", "service")
            .order_by("start_time")
        )

        return Response(TimeSlotSerializer(slots, many=True).data)

