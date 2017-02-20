from .models import Event, EventActivity
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Event
        depth = 1
        fields = ("pk", "name", "image", "datetime", "address", "description", "is_active", "is_upcoming", "location")


class EventSimpleSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    image = serializers.CharField(allow_blank=True, required=False)
    datetime = serializers.DateTimeField(required=False)
    address = serializers.CharField(allow_blank=True, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    is_registered = serializers.BooleanField()


class EventActivitySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EventActivity
