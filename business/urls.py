from django.urls import path
from .views import *


urlpatterns = [
    path('business', BusinessView.as_view(), name='businesses'),
    path('business/<business_id>', BusinessDetailsView.as_view(), name='business_details'),
]