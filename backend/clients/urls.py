from django.urls import path
from clients.views import ClientListCreateView,ClientListDebtsView

urlpatterns = [
    path('', ClientListCreateView.as_view(), name='client-list'),
    path('<uuid:id>/debts/', ClientListDebtsView.as_view(), name='client-debts')
]
