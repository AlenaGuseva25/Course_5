from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from users.serializers import TokenSerializer, UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    '''Получение токена'''
    serializer_class = TokenSerializer


class UserCreateAPIView(generics.CreateAPIView):
    '''Регистрация нового пользователя'''
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def perform_create(self, serializer):
        '''Хеш пароля'''
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()


class UserListAPIView(generics.ListAPIView):
    '''Список зарегистированных пользователей'''
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    '''Детальная информация по пользователю'''
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    '''Изменение информацию по пользователю'''
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    '''Удаление информации по пользователю'''
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
