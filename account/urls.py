from django.urls import path
from .views import *

urlpatterns = [
    path('account/login', LoginView.as_view(), name='login'),
    path('account/logout/', logout, name='logout'),
    path('account/profile/', ProfileView.as_view(), name='profile'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('search/', search, name='search'),
    path('analytics/', analytics, name='analytics'),
    path('account_deletion/<user_id>/<user_type>', account_deletion, name='account_deletion'),

]
