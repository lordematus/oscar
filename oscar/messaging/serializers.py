from django.contrib.auth.models import User
from rest_framework import serializers

from messaging.models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')
    recipient = serializers.CharField(source='recipient.username')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'content', 'timestamp']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
