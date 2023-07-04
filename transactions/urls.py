from django.urls import path
from .views import TransactionsListView, WithdrawalListView, WithdrawalDetailsView, EarningListView

urlpatterns = [
    path('transactions', TransactionsListView.as_view(), name='transactions'),
    path('withdrawals', WithdrawalListView.as_view(), name='withdrawals'),
    path('earnings', EarningListView.as_view(), name='earnings'),
]