from django.urls import path
from ..orders.views import process_order, order_thanks
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<slug:item_slug>/', views.add_to_cart, name='add_to_cart'),  # Изменено на slug
    path('delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('create-order/', process_order, name='create_order'),
    path('order-form/', views.order_form, name='order_form'),
    path('order-thanks/', order_thanks, name='order_thanks'),

]
