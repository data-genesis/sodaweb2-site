from django.urls import path

from .views import item_details, store

app_name = 'store'

urlpatterns = [
    path('', store, name='home'),
    path('<slug:item_slug>/', item_details, name='item_details'),
]
