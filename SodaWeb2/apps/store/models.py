from django.db import models
from django.utils.translation import gettext_lazy as _


class Photo(models.Model):
    item = models.ForeignKey('Item', related_name='photos', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='items_photos/')  # Измените путь, если нужно

    def __str__(self):
        return f"Фото для {self.item.title if self.item else 'неуказанного товара'}"


class Item(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название',)
    description = models.TextField(verbose_name='Описание',)
    slug = models.CharField(
        unique=True,
        max_length=50,
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления',)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Новая цена',
    )
    old_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Старая цена',
        blank=True,
        null=True,
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступно',
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-price']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'