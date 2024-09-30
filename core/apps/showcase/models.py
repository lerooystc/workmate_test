from apps.showcase.choices import CAT_COLOR_CHOICES
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class OwnedModel(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Breed(models.Model):
    """Породы котов"""

    name = models.CharField(verbose_name="Наименование породы", max_length=50)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Порода кота"
        verbose_name_plural = "Породы котов"


class Cat(OwnedModel):
    """Коты"""

    name = models.CharField(verbose_name="Имя", max_length=50)
    color = models.PositiveSmallIntegerField(
        verbose_name="Цвет", choices=CAT_COLOR_CHOICES
    )
    age = models.PositiveSmallIntegerField(
        verbose_name="Возраст",
        validators=[MaxValueValidator(240), MinValueValidator(1)],
    )
    description = models.TextField(verbose_name="Описание", default="Описания нет.")
    breed = models.ForeignKey(
        Breed, on_delete=models.CASCADE, verbose_name="Порода", related_name="cats"
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.age} месяцев"

    class Meta:
        verbose_name = "Кот"
        verbose_name_plural = "Коты"
