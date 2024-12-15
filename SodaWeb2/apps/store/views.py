from django.shortcuts import get_object_or_404, render
from .models import Photo
from .models import Item


def store(request):
    photos = Photo.objects.all()
    items = Item.objects.filter(is_available=True)
    context = {
        'photos': photos,
        'items': items,  # Передаем все доступные товары
        'range': [*range(1, len(items) + 1)],  # Динамический диапазон для стилей
    }

    print(items)
    return render(request, 'store/main_page.html', context)


def item_details(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    # Получаем все фотографии для данного товара
    photos = item.photos.all()
    context = {
        'item': item,
        'photos': photos,  # Добавляем фотографии в контекст
    }
    return render(request, 'store/item_details.html', context)

