from django.urls import path
from . views import *

urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('expense/',ExpenseListCreateView.as_view(),name='expense'),
    path('balances/<int:user_id>/', BalanceListView.as_view(), name='balance-list'),
]
