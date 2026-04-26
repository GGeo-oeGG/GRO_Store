from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Отображение пользователя в админ панели."""

    list_display = [
        "email",
        "name",
        "created_at",
    ]

    search_fields = ("name",)
    readonly_fields = ["created_at", "updated_at"]
