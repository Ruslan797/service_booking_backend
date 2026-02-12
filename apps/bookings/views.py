from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.services.models import TimeSlot
from .models import Booking
from .serializers import BookingCreateSerializer, BookingListSerializer


class MyBookingListView(generics.ListAPIView):
    """
    GET /api/bookings/
    Показываем только брони текущего пользователя.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingListSerializer

    def get_queryset(self):
        return (
            Booking.objects
            .filter(user=self.request.user)
            .select_related(
                "time_slot",
                "time_slot__service",
                "time_slot__specialist",
                "time_slot__specialist__provider",
            )
            .order_by("-created_at")
        )


class BookingCreateView(generics.CreateAPIView):
    """
    POST /api/bookings/
    Body: { "time_slot": <id> }
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        time_slot_id = serializer.validated_data["time_slot"].id

        # 1) Блокируем строку time_slot в транзакции (ключевой момент!)
        try:
            slot = (
                TimeSlot.objects
                .select_for_update()
                .select_related("specialist", "specialist__provider", "service")
                .get(id=time_slot_id)
            )
        except TimeSlot.DoesNotExist:
            return Response({"detail": "Time slot not found."}, status=status.HTTP_404_NOT_FOUND)

        # 2) Проверяем, свободен ли слот
        if slot.is_booked:
            return Response({"detail": "This time slot is already booked."}, status=status.HTTP_400_BAD_REQUEST)

        # 3) Создаём Booking (OneToOne гарантирует 1 бронь на слот)
        booking = Booking.objects.create(user=request.user, time_slot=slot)

        # 4) Помечаем слот как занятый
        slot.is_booked = True
        slot.save(update_fields=["is_booked"])

        # 5) Отдаём красивый ответ
        out = BookingListSerializer(booking).data
        return Response(out, status=status.HTTP_201_CREATED)

