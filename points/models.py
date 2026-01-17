"""
Модели
"""

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Point(models.Model):
    name = models.CharField(max_length=50, verbose_name="название точки")
    description = models.CharField(max_length=256, blank=True, verbose_name="описание точки")
    latitude = models.FloatField(verbose_name="широта")
    longitude = models.FloatField(verbose_name="долгота")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="создатель точки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата обновления")
    
    class Meta:
        verbose_name = "гео-точка"
        verbose_name_plural = "гео-точки"

    def __str__(self):
        """
        Возвращает точку в строке
        """
        return self.name
    
    
class Message(models.Model):
    text = models.CharField(max_length=256, verbose_name="текст сообщения")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор сообщения")
    point = models.ForeignKey(Point, on_delete=models.CASCADE, verbose_name="гео-точка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата обновления")
    
    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"

    def __str__(self):
        """
        Возвращает сообщение в строке
        """
        return self.text
