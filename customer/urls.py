from django.urls import path
from .views import *


urlpatterns = [
    path('customers', CustomersView.as_view(), name='customers'),
    path('customer/<user_id>', CustomerDetailsView.as_view(), name='customer'),
    path('customer/account/<user_id>/<action>/', customer_kyc, name='customer_control'),
    path('customer/<user_id>/<image_id>/<remark>', delete_file, name='delete_customer_files'),
]