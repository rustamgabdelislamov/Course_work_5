from django.urls import path

from habit.apps import HabitConfig
from habit.views import (
    HabitCreateAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    HabitsDestroyAPIView,
)

app_name = HabitConfig.name

urlpatterns = [
    path("create/", HabitCreateAPIView.as_view(), name="habit_create"),
    path("", HabitListAPIView.as_view(), name="habit_list"),
    path("retrieve/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit_retrieve"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("delete/<int:pk>/", HabitsDestroyAPIView.as_view(), name="habit_delete"),
]
