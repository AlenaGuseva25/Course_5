from django.urls import path
from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    PublicHabitViewSet
)
from rest_framework.routers import DefaultRouter

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"public-habits", PublicHabitViewSet, basename="public-habits")

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habit-list'),
    path('habits/create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('habits/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit-retrieve'),
    path('habits/<int:pk>/update/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('habits/<int:pk>/destroy/', HabitDestroyAPIView.as_view(), name='habit-destroy'),
] + router.urls