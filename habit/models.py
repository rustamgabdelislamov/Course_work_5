from datetime import timedelta

from django.db import models
from django.conf import settings


class Habits(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Создатель привычки",
        related_name= "user"
    )
    place = models.CharField(verbose_name="Место выполнения", blank=True, null=True)
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(verbose_name="Действие привычки")
    reward_action = models.BooleanField(
        default=True, verbose_name="Признак приятной привычки"
    )
    addition_habit = models.ForeignKey(
        "self",
        verbose_name="Связанная привычка",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    period = models.PositiveIntegerField(
        default=1, verbose_name="Число повторений в неделю"
    )
    award = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Вознаграждение"
    )
    time_to_action = models.TimeField(
        default=timedelta(minutes=2), verbose_name="Время на выполнение"
    )
    is_published = models.BooleanField(default=True, verbose_name="Признак публичности")

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"
