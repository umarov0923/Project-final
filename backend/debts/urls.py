from django.urls import path
from .views import (
    DebtListCreateView,
    DebtDetailView, DebtDetailPaymentView
)

urlpatterns = [
    path('', DebtListCreateView.as_view(), name='debt-list-create'),
    path('<int:pk>/', DebtDetailView.as_view(), name='debt-detail'),
    path('<int:id>/payments/', DebtDetailPaymentView.as_view(), name='debt-payments'
    ),
]