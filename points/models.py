"""
Модели для гео-точек
"""

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Point(models.Model):
    """
    Attributes:
        name(CharField): Название точки
        description(CharField): Описание точки
        latitude(FloatField): Широта
        longitude(FloatField): Долгота
        creator(ForeignKey): Создатель точки
        created_at(DateTimeField): Дата создания точки
        updated_at(DateTimeField): Дата последнего изменения точки

    Meta:
        verbose_name (str): Название модели в единственном числе
        verbose_name_plural (str): Название модели во множественном числе
    """

    name = models.CharField(max_length=50, verbose_name="название точки")
    description = models.CharField(
        max_length=256, blank=True, verbose_name="описание точки"
    )
    latitude = models.FloatField(verbose_name="широта")
    longitude = models.FloatField(verbose_name="долгота")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="создатель точки"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата обновления")

    class Meta:
        verbose_name = "гео-точка"
        verbose_name_plural = "гео-точки"

    def __str__(self) -> str:
        """
        Возвращает точку в строке
        """
        return self.name


class Message(models.Model):
    """
    Attributes:
        text(CharField): Текст сообщения
        author(ForeignKey): Автор сообщения
        point(ForeignKey): Точка для сообщения
        created_at(DateTimeField): Дата создания сообщения
        updated_at(DateTimeField): Дата последнего изменения сообщения

    Meta:
        verbose_name (str): Название модели в единственном числе
        verbose_name_plural (str): Название модели во множественном числе
    """

    text = models.CharField(max_length=256, verbose_name="текст сообщения")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="автор сообщения"
    )
    point = models.ForeignKey(Point, on_delete=models.CASCADE, verbose_name="гео-точка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата обновления")

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"

    def __str__(self) -> str:
        """
        Возвращает сообщение в строке
        """
        return self.text
