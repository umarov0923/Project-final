from rest_framework import serializers
from payments.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["user"]  # Делаем поле user доступным только для чтения

    def create(self, validated_data):
        """Устанавливаем текущего пользователя автоматически"""
        request = self.context.get("request")
        if request.user.company == validated_data['debt'].client.company:
            validated_data["user"] = request.user
        return super().create(validated_data)
