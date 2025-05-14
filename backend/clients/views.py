from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from clients.models import Client
from clients.serializers import ClientSerializer, DebtSerializer
from django.shortcuts import get_object_or_404



class ClientListCreateView(generics.ListCreateAPIView):
    """Просмотр списка клиентов и добавление нового"""
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.company:
            return Client.objects.filter(company=user.company)
        else:
            raise ValueError("У пользователя нет связанной компании.")



class ClientListDebtsView(APIView):
    """Просмотр задолженности конкретного клиента + сам клиент один раз"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        client = get_object_or_404(Client, id=id)

        if client.company != request.user.company:
            raise PermissionDenied("У вас нет доступа к задолженности этого клиента.")

        debts = client.debts.all()
        client_data = ClientSerializer(client).data
        debts_data = DebtSerializer(debts, many=True).data

        return Response({
            "client": client_data,
            "debts": debts_data
        })