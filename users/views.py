from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import CustomUser
from users.serializers import CustomUserSerializer, ClassModerSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
        original_password = serializer.validated_data['password']
        # print(f"User created: {user.email}, Password (hashed): {user.password}")
        user = authenticate(email=user.email, password=original_password)
        # print(f"Authenticated user: {user}")
        if user is not None:
            login(self.request, user)


class CustomUserListAPIView(generics.ListAPIView):
    serializer_class = ClassModerSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("is_active",)
    ordering_fields = ("email",)


class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClassModerSerializer

    def get_serializer_class(self):
        # Получаем объект пользователя
        obj = self.get_object()
        if self.request.user == obj:
            return CustomUserSerializer  # полный сериализатор для владельца
        return super().get_serializer_class()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("is_active",)
    ordering_fields = ("email",)


class CustomUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class CustomUserDestroyAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
