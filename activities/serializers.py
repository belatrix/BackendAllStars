from .models import Message, Activity
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='from_user.avatar')

    class Meta:
        model = Message
        fields = ('id', 'datetime', 'text', 'to_user', 'from_user', 'avatar')


class ActivitySerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='to_user.avatar')

    class Meta:
        model = Activity
        fields = ('id', 'datetime', 'text', 'to_user', 'avatar')


class NotificationSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    text = serializers.CharField()
    avatar = serializers.CharField()
