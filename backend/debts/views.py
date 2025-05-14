from rest_framework import generics, permissions
from debts.models import Debt
from .serializers import DebtSerializer, PaymentSerializer
from payments.models import Payment
from django.utils.timezone import now

from django.utils import timezone
from rest_framework import permissions
from rest_framework import generics
from .models import Debt
from .serializers import DebtSerializer

class DebtListCreateView(generics.ListCreateAPIView):
    """Просмотр списка задолженностей и добавление нового долга"""
    serializer_class = DebtSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'company') or user.company is None:
            return Debt.objects.none()

        # Получаем фильтр из параметров запроса
        filter_type = self.request.query_params.get('filter', 'all')

        # Все долги
        if filter_type == 'all':
            return Debt.objects.filter(client__company=user.company)
        
        # Просроченные долги
        elif filter_type == 'overdue':
            today = timezone.now().date()
            return Debt.objects.filter(client__company=user.company, due_date__lt=today, is_paid=False)

        return Debt.objects.none()

    def perform_create(self, serializer):
        """Метод для добавления нового долга"""
        serializer.save()


class DebtDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, обновление и удаление задолженности"""
    serializer_class = DebtSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'company') or user.company is None:
            return Debt.objects.none()
        return Debt.objects.filter(client__company=user.company)
    

class DebtDetailPaymentView(generics.ListAPIView):
    """Просмотр платежей по конкретной задолженности"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        debt_id = self.kwargs['id']
        user = self.request.user

        try:
            debt = Debt.objects.get(id=debt_id)
        except Debt.DoesNotExist:
            return Payment.objects.none()

        if not hasattr(user, 'company') or user.company is None:
            return Payment.objects.none()

        if debt.client.company != user.company:
            return Payment.objects.none()

        return debt.payments.all()
    

