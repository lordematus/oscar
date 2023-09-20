from django.contrib.auth.models import User
from django.db import models
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from messaging.models import Message
from messaging.serializers import UserSerializer, MessageSerializer


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ['register', 'login']:
            permission_classes = [AllowAny]
        return permission_classes

    @action(detail=False, methods=['post'])
    def register(self, request, pk=None):
        pass

    @action(detail=False, methods=['post'])
    def login(self, request, pk=None):
        pass

    @action(detail=False, methods=['post'])
    def logout(self, request, pk=None):
        pass


class MessageViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            models.Q(sender=user) | models.Q(recipient=user)
        ).order_by('timestamp').reverse()
