from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Отображение и управление пользователем в админ панели."""

    ordering = ("email",)
    list_display = [
        "email",
        "name",
        "created_at",
    ]

    search_fields = ("name", "email")
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("name", "created_at", "updated_at")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительно", {"fields": ("name",)}),
    )
