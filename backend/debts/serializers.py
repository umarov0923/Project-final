from rest_framework import serializers
from debts.models import Debt
from clients.models import Client
from payments.models import Payment
from datetime import date


class DebtSerializer(serializers.ModelSerializer):
    """Сериализатор для модели задолженности"""
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.none())

    class Meta:
        model = Debt
        fields = '__all__'
        read_only_fields = ('is_paid', 'remaining_amount')
        depth = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['client'].queryset = Client.objects.filter(company=request.user.company)

    def validate(self, attrs):
        """Проверка на отрицательные значения"""
        if attrs.get('total_amount') < 0:
            raise serializers.ValidationError("Сумма долга не может быть отрицательной.")
        
        due_date = attrs.get('due_date')
        if due_date and due_date <= date.today():
            raise serializers.ValidationError("Срок должен быть позже сегодняшнего дня.")
    
        return attrs


    

class PaymentSerializer(serializers.ModelSerializer):
    # Add a field to include debt.total_amount
    debt_total_amount = serializers.DecimalField(
        source="debt.total_amount",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    user_email = serializers.CharField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = Payment
        fields = "__all__"  # Includes all fields from Payment model
        read_only_fields = ["user", "debt_total_amount"]  # Make user and debt_total_amount read-only

    def create(self, validated_data):
        """Устанавливаем текущего пользователя автоматически"""
        request = self.context.get("request")
        if request and request.user:
            validated_data["user"] = request.user
        return super().create(validated_data)