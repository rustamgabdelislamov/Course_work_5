from django.contrib import admin

from habit.models import Habits


@admin.register(Habits)
class HabitsAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "id",
        "owner",
    )  # Поля, которые будут отображаться в списке
    search_fields = ("action",)
