from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from messaging.models import Message
from messaging.serializers import UserSerializer, MessageSerializer, RegistrationSerializer


class LoginViewSet(GenericViewSet):
    @action(detail=False, methods=['post'], permissions=[AllowAny])
    def login(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=self.get_success_headers(serializer.data)
        )

    @action(detail=False, methods=['post'], permissions=[IsAuthenticated])
    def logout(self, request, pk=None):
        logout(request)
        return Response({'message': 'logout sucessful'})


class RegistrationViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    authentication_classes = [AllowAny]


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]


class MessageViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            models.Q(sender=user) | models.Q(recipient=user)
        ).order_by('timestamp').reverse()
