from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habit.models import Habits
from habit.paginators import HabitsPaginator
from habit.permissions import IsAdmin, IsOwner
from habit.serializers import HabitsSerializer, HabitsModerationSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitsSerializer
    pagination_class = HabitsPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Habits.objects.all()

        if user.is_staff or user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=user) | queryset.filter(is_published=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Habits.objects.all()

        if user.is_staff or user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=user) | queryset.filter(is_published=True)


class HabitUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsOwner]
    queryset = Habits.objects.all()

    def get_serializer_class(self):
        habit = self.get_object()
        if self.request.user == habit.owner:
            return HabitsSerializer
        else:
            return HabitsModerationSerializer


class HabitsDestroyAPIView(generics.DestroyAPIView):
    queryset = Habits.objects.all()
    permission_classes = [IsOwner]

