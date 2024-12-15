from django.urls import path
from .views import process_order
from ..cart.views import order_form
app_name = 'orders'

urlpatterns = [
    path('process-order/', process_order, name='process_order'),
    path("order_form", order_form, name="order_form")
]