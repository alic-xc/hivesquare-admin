from django.urls import path
from .views import *


urlpatterns = [
    path('slideshow', SlideShowView.as_view(), name='slideshow'),
    path('ads', AdsView.as_view(), name='ads'),
    path('category', CategoryView.as_view(), name='category'),
    path('action/<object_id>/<object_type>/delete', delete_action, name='delete_action'),
    path('sub-category', SubCategoryView.as_view(), name='sub-category'),
    path('business-category', BusinessCategoryView.as_view(), name='business-category'),
    path('subscription', SubscriptionView.as_view(), name='subscription'),

]