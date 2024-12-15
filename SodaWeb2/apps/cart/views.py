from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.http import HttpResponseRedirect

from .models import CartItem
from ..store.models import Item
from ..orders.models import Order
from ..orders.forms import OrderForm


def cart(request):

    session_key = request.session.session_key

    cart_items = CartItem.objects.filter(cart=session_key)
    total_price = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    print(cart_items)
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)

    # Получаем сессию пользователя
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    session = Session.objects.get(session_key=session_key)

    # Проверяем, существует ли уже данный товар в корзине
    cart_item, created = CartItem.objects.get_or_create(item=item, cart=session)
    if not created:
        # Если товар уже есть в корзине, увеличиваем количество
        cart_item.quantity += 1
    else:
        # Если товар новый, устанавливаем количество 1
        cart_item.quantity = 1

    cart_item.save()

    # Обновляем количество товаров в корзине
    cart_items_count = CartItem.objects.filter(cart=session).count()

    # Возвращаем JSON ответ
    return JsonResponse({
        'success': True,
        'message': 'Товар успешно добавлен в корзину',
        'cart_items_count': cart_items_count
    })



def create_order(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(cart=session_key)

    if cart_items.exists():
        # Создаем новый заказ
        ordered_items = []
        for cart_item in cart_items:
            ordered_items.append({
                'id': cart_item.item.id,
                'name': cart_item.item.title,
                'price': str(cart_item.item.price),
                'quantity': cart_item.quantity
            })

        order = Order.objects.create(
            ordered_items=ordered_items,  # Предполагается, что это JSONField в модели Order
            quantity=sum(item.quantity for item in cart_items),
            order_price=sum(item.total_price() for item in cart_items)
        )

        # Очищаем корзину
        cart_items.delete()

        return JsonResponse({
            'success': True,
            'message': f'Заказ {order.order_number} успешно создан',
            'order_number': order.order_number  # Используем order_number вместо id
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Ваша корзина пуста'
        })


def delete_cart_item(request, item_id):
    session_key = request.session.session_key
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__session_key=session_key)

        cart_item = get_object_or_404(CartItem, id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Товар не найден'}, status=400)

def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Создаем заказ с данными из формы
            cart_items = CartItem.objects.filter(cart=request.session.session_key)
            if not cart_items:
                # Обработка случая, когда корзина пуста
                return render(request, 'cart/order_form.html', {'form': form, 'error': 'Ваша корзина пуста'})

            ordered_items = []
            for item in cart_items:
                ordered_items.append({
                    'id': item.item.id,
                    'name': item.item.title,
                    'price': str(item.item.price),
                    'quantity': item.quantity
                })

            order = Order.objects.create(
                user_id=form.cleaned_data['name'],
                user_phone=form.cleaned_data['phone'],
                user_tg=form.cleaned_data['tg_username'],
                ordered_items=ordered_items,
                quantity=sum(item.quantity for item in cart_items),
                order_price=sum(item.total_price() for item in cart_items)
            )

            # Очищаем корзину после создания заказа
            cart_items.delete()

            # Перенаправление на страницу благодарности или показ сообщения
            return render(request, 'cart/order_thanks.html', {'order_number': order.order_number})
    else:
        form = OrderForm()

    return render(request, 'cart/order_form.html', {'form': form})