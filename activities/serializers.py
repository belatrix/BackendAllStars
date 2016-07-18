from .models import Message, Activity
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity


class NotificationSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    text = serializers.CharField()
