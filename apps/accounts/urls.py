from django.urls import path
from .views import RegisterView, MeView, UserRoleUpdateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("users/<int:pk>/role/", UserRoleUpdateView.as_view(), name="user-role-update"),
]
