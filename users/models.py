from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите email"
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Необязательное поле. Введите номер телефона",
    )
    image = models.ImageField(
        upload_to="users/image", verbose_name="Фото", blank=True, null=True
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Необязательное поле. Введите город",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активность",
        blank=True,
        null=True,
    )
    tg_chat_id = models.CharField(
        max_length=100,
        verbose_name="телеграмм id",
        blank=True,
        null=True,
        help_text="Необязательное поле. Введите телеграм id",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
