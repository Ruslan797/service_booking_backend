from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Регистрация пользователя.
    Пароль сохраняем через set_password().
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data, password=password)
        return user


class MeSerializer(serializers.ModelSerializer):
    """
    Чтение профиля текущего пользователя
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        )


class MeUpdateSerializer(serializers.ModelSerializer):
    """
    Обновление профиля текущего пользователя
    """

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("role",)

    def validate_role(self, value):
        allowed = {"client", "provider"}
        if value not in allowed:
            raise serializers.ValidationError(f"role must be one of: {sorted(allowed)}")
        return value
