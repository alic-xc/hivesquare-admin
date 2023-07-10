from django.urls import path
from .views import *


urlpatterns = [
    path('orders', OrdersView.as_view(), name='orders'),
    path('order/<order_id>', OrderDetailsView.as_view(), name='order'),
]