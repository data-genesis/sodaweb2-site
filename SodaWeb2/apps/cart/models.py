from django.db import models
from django.contrib.sessions.models import Session  # Импорт модели Session
from ..store.models import Item  # Импорт модели товара

class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Session, on_delete=models.CASCADE, default=1)  # Связь с сессией

    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.item.title} (x{self.quantity})"
