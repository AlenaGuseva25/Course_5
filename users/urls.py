from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserUpdateAPIView,
    MyTokenObtainPairView,
    UserRetrieveAPIView,
)


app_name = UsersConfig.name

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Пользователи
    path('', UserListAPIView.as_view(), name='users_list'),
    path('register/', UserCreateAPIView.as_view(), name='register'),

    # Работа с конкретным пользователем
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),
]
