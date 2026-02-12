from django.urls import path
from .views import MyBookingListView, BookingCreateView

urlpatterns = [
    path("", MyBookingListView.as_view(), name="booking-list"),
    path("create/", BookingCreateView.as_view(), name="booking-create"),
]
