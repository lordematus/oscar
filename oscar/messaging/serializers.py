from django.contrib.auth.models import User
from rest_framework import serializers

from messaging.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        field = ['sender', 'recipient', 'content', 'timestamp']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ['username', 'password', 'email']
