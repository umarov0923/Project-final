from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserRegistrationSerializer, UserLoginSerializer, TokenRefreshSerializer, UserSerializer


class UserRegistrationView(APIView):
    """ Регистрация нового пользователя """
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            
            return Response({
              "messsage": "Пользователь успешно зарегистрирован",
              "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """ Вход в систему и выдача токенов """
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        user = serializer.validated_data  # Теперь это объект User
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": UserSerializer(user).data,  # Если нужно вернуть информацию о пользователе
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)

class TokenRefreshView(APIView):
    """ Обновление JWT-токена """
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """ Получение данных о текущем пользователе """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    
