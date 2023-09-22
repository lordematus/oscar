from django.contrib.auth.validators import validate_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from messaging.models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'content', 'timestamp']

    def validate_recipient(self, recipient):
        if self.context['request'].user == recipient:
            raise serializers.ValidationError("cannot send message to yourself")
        return recipient


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("username already exists")
        return username

    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return password

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
