from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("Название", max_length=50, unique=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст", blank=True)
    is_done = models.BooleanField("Выполнено", default=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, related_name="notes", verbose_name="Автор",
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="notes", verbose_name="Категория",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="notes", verbose_name="Теги")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"

    def __str__(self):
        return self.title