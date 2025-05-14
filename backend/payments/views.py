from django.shortcuts import render
from rest_framework import generics, permissions
from payments.models import Payment
from payments.serializers import PaymentSerializer



class PaymentListCreateView(generics.ListCreateAPIView):
    """Просмотр списка оплат и добавление новой оплаты"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'company') or user.company is None:
            return Payment.objects.none()
        return Payment.objects.filter(debt__client__company=user.company)

    def perform_create(self, serializer):
        """Автоматически добавляет текущего пользователя"""
        serializer.save(user=self.request.user)

    

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, обновление и удаление оплаты"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'company') or user.company is None:
            return Payment.objects.none()
        return Payment.objects.filter(debt__client__company=user.company)


# Create your views here.
