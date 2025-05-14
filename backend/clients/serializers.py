from rest_framework import serializers
from clients.models import Client
from rest_framework.exceptions import ValidationError
from debts.models import Debt


class ClientSerializer(serializers.ModelSerializer):
    """Сериализатор клиента"""
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        user = self.context['request'].user

        if not user.company:
            raise ValidationError("У пользователя нет связанной компании.")
        
        company = user.company
        validated_data['company'] = company
        return super().create(validated_data)


class DebtSerializer(serializers.ModelSerializer):
    """Сериализатор для модели задолженности"""
    client = ClientSerializer()
    
    class Meta:
        model = Debt
        fields = '__all__'
        read_only_fields = ('is_paid', 'remaining_amount')
        depth = 1
    
    def validate(self, attrs):
        """Проверка на отрицательные значения"""
        if attrs.get('total_amount') < 0:
            raise serializers.ValidationError("Сумма долга не может быть отрицательной.")
        return attrs

