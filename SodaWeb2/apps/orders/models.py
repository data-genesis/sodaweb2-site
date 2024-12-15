# orders/models.py
import random
from django.db import models
from django.utils import timezone
from apps.store.models import Item

def generate_order_id():
    letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    return f"{letter}{numbers}"

class Order(models.Model):
    order_number = models.CharField(max_length=6, default=generate_order_id, unique=True, editable=False)
    user_id = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=20)
    user_tg = models.CharField(max_length=50, blank=True, null=True)  # Ник в Telegram
    ordered_items = models.JSONField(default=list)  # Список товаров в заказе
    quantity = models.PositiveIntegerField(default=1)  # Общее количество товаров
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.order_number}"