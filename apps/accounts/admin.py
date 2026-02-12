from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    #  главное: убираем username из сортировки
    ordering = ("email",)

    #  что показываем в списке пользователей
    list_display = ("id", "email", "role", "is_staff", "is_superuser", "is_active")
    search_fields = ("email",)
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    #  поля на странице редактирования пользователя
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Role"), {"fields": ("role",)}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    #  поля на странице создания пользователя в админке
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role", "is_staff", "is_superuser", "is_active"),
            },
        ),
    )

    #  говорим админке: логин — email (username поля нет)
    # Это влияет на форму добавления и на поведение админки
    username_field = "email"


