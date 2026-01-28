from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import HabitSerializer
from .paginators import HabitPaginator

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(user=user)

class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
