from habits.models import Habit
from habits.paginators import Pagination
from habits.permissions import OwnerOrReadOnly
from habits.serializers import HabitSerializer, PublicHabitSerializer
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    '''Доступ к просмотру привычек другими пользователями'''
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = PublicHabitSerializer
    permission_classes = [AllowAny]


class HabitListAPIView(generics.ListAPIView):
    '''Доступ только к собственным привычкам'''
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    '''Закрытый доступ к выбранной привычке'''
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, OwnerOrReadOnly]


class HabitCreateAPIView(generics.CreateAPIView):
    '''Создание привычки только авторизованными пользователями'''
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]


class HabitUpdateAPIView(generics.UpdateAPIView):
    '''Изменение привычки только владельцем'''
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, OwnerOrReadOnly]
    queryset = Habit.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    '''Удаление привычки только владельцем'''
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, OwnerOrReadOnly]
    queryset = Habit.objects.all()