from .models import Event
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        depth = 1
        fields = ('pk',
                  'title',
                  'description',
                  'datetime',
                  'location',
                  'collaborators',
                  'participants')


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('pk',
                  'title',
                  'description',
                  'datetime',
                  'location',
                  'collaborators',
                  'participants')

