from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user_id', 'user_phone', 'user_tg', 'quantity', 'order_price', 'created_at')
    search_fields = ('order_number', 'user_id', 'user_phone', 'user_tg')
    list_filter = ('created_at',)
    readonly_fields = ('order_number', 'ordered_items')

    def get_ordering(self, request):
        return ['-created_at']  # Сортировка по дате создания в обратном порядке

    def created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
    created_at.short_description = 'Дата создания'
    created_at.admin_order_field = 'created_at'

    def has_add_permission(self, request):
        return False  # Запрещаем добавление новых заказов через админку

    def has_change_permission(self, request, obj=None):
        return False  # Запрещаем изменение заказов через админку

    def has_delete_permission(self, request, obj=None):
        return False  # Запрещаем удаление заказов через админку