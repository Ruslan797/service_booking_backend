from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import (
    RegisterSerializer,
    MeSerializer,
    MeUpdateSerializer,
    UserRoleUpdateSerializer,
)

User = get_user_model()


class MeView(RetrieveUpdateAPIView):
    """
    GET  /api/accounts/me/    -> показать текущего пользователя
    PATCH /api/accounts/me/   -> обновить first_name/last_name текущего пользователя
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return MeUpdateSerializer
        return MeSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/ -> регистрация нового пользователя
    """

    serializer_class = RegisterSerializer
    permission_classes = ()  # регистрация доступна без токена


class UserRoleUpdateView(generics.UpdateAPIView):
    """
    PATCH /api/accounts/users/<id>/role/ -> админ меняет role
    """

    queryset = User.objects.all()
    serializer_class = UserRoleUpdateSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ["patch"]
