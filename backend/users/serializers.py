from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации пользователя """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'confirm_password', 'user_roles', 'username')

    def validate(self, data):
        data['email'] = data['email'].lower()  # Приводим email к нижнему регистру
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Пароли не совпадают!"})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)  # Используем create_user()
    

class UserLoginSerializer(serializers.Serializer):
    """ Сериализатор для входа в систему """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email'].lower()  # Приводим email к нижнему регистру
        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(data['password']):
            raise serializers.ValidationError("Неверные учетные данные")

        return user  # ДОЛЖЕН ВОЗВРАЩАТЬ ОБЪЕКТ USER, А НЕ DICT



class TokenRefreshSerializer(serializers.Serializer):
    """ Сериализатор для обновления токена """
    refresh = serializers.CharField()

    def validate(self, data):
        try:
            refresh = RefreshToken(data['refresh'])
            return {'access': str(refresh.access_token)}
        except Exception:
            raise serializers.ValidationError("Невалидный refresh-токен")



class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для получения информации о пользователе """

    class Meta:
        model = User
        fields = ('id', 'email', 'user_roles', 'full_name')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

