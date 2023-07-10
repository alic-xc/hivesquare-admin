from django.urls import path
from .views import *


urlpatterns = [
    path('products', ProductsView.as_view(), name='products'),
    path('product/<product_id>', ProductDetailsView.as_view(), name='product'),
    path('product/update/<product_id>/<action>/', product_kyc, name='product_control'),
    # path('customer/<user_id>/<image_id>/<remark>', delete_file, name='delete_customer_files'),
]