from django.urls import path
from .views import *


urlpatterns = [
    path('vendors', VendorView.as_view(), name='vendors'),
    path('vendor/<user_id>', VendorDetailsView.as_view(), name='vendor'),
    path('vendor/account/<user_id>/<action>/', vendor_kyc, name='vendor_control'),
]