from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import OrderForm
from .models import Order
from ..cart.models import CartItem
from django.contrib import messages


def process_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cart_items = CartItem.objects.filter(cart=request.session.session_key)
            if not cart_items:
                return JsonResponse({'success': False, 'message': 'Корзина пуста'})

            # Создаем заказ
            ordered_items = []
            for item in cart_items:
                ordered_items.append({
                    'id': item.item.id,
                    'name': item.item.title,
                    'price': str(item.item.price),
                    'quantity': item.quantity
                })

            order = Order.objects.create(
                user_id=form.cleaned_data['name'],  # Используем имя как ID
                user_phone=form.cleaned_data['phone'],
                user_tg=form.cleaned_data['tg_username'],
                ordered_items=ordered_items,
                quantity=sum(item.quantity for item in cart_items),
                order_price=sum(item.total_price() for item in cart_items)
            )

            # Очищаем корзину
            cart_items.delete()

            # Отправляем пользователю order_number вместо order_id
            return JsonResponse({
                'success': True,
                'message': f'Заказ успешно создан. Номер заказа: {order.order_number}',
                'order_number': order.order_number
            })
        else:
            # В случае ошибок валидации
            return JsonResponse({'success': False, 'message': 'Ошибка в данных формы'})
    else:
        form = OrderForm()
        return render(request, 'cart/orders.html', {'form': form})


def order_thanks(request):
    return render(request, 'cart/order_thanks.html')


