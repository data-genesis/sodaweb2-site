from django.contrib import admin
from .models import Item, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1  # Количество лишних форм для добавления новых фотографий


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'slug', 'price', 'old_price', 'is_available',)
    search_fields = ('title', 'description',)
    list_filter = ('is_available',)
    inlines = [PhotoInline]  # Добавляем встроенную форму для фотографий

    def short_description(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + '...'
        else:
            return obj.description

    short_description.short_description = 'Описание'


admin.site.register(Item, ItemAdmin)
# Photo больше не регистрируем отдельно, так как она теперь связана с Item