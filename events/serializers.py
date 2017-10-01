from .models import Event, EventActivity
from employees.serializers import LocationSerializer
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta(object):
        model = Event
        depth = 1
        fields = ("pk",
                  "name",
                  "image",
                  "datetime",
                  "address",
                  "registration_url",
                  "description", "is_active",
                  "location")


class EventSimpleSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    image = serializers.CharField(allow_blank=True, required=False)
    datetime = serializers.DateTimeField(required=False)
    address = serializers.CharField(allow_blank=True, required=False)
    registration_url = serializers.CharField(allow_blank=True, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    is_registered = serializers.BooleanField()


class EventActivitySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EventActivity
        fields = ("pk", "datetime", "text", "event")
