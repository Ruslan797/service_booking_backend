from django.urls import path
from .views import ServiceListCreateView, TimeSlotListView, AvailableSlotsView

urlpatterns = [
    path("services/", ServiceListCreateView.as_view(), name="services"),
    path("time-slots/", TimeSlotListView.as_view(), name="time-slots"),
    path("<int:service_id>/available/", AvailableSlotsView.as_view(), name="available-slots"),
]

