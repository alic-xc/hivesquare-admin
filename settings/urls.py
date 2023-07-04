from django.urls import path
from .views import *


urlpatterns = [
    path('slideshow', SlideShowView.as_view(), name='slideshow'),
    path('category', CategoryView.as_view(), name='category'),
    path('sub-category', SubCategoryView.as_view(), name='sub-category'),
    path('subscription', SubscriptionView.as_view(), name='subscription'),
]