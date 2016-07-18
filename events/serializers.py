from .models import Attendance, Event, Participant
from employees.models import Employee
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    collaborators = serializers.IntegerField(source='num_collaborators')
    participants = serializers.IntegerField(source='num_participants')

    class Meta:
        model = Event
        fields = ('pk',
                  'title',
                  'description',
                  'datetime',
                  'image',
                  'location',
                  'is_registration_open',
                  'collaborators',
                  'participants')


class EventSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('pk', 'title', 'image', 'is_registration_open')


class EventSimpleRegistrationSerializer(serializers.ModelSerializer):
    is_registered = serializers.SerializerMethodField()

    def get_is_registered(self, obj):
        return True

    class Meta:
        model = Event
        fields = ('pk', 'title', 'image', 'is_registration_open', 'is_registered')


class EventSimpleUnregistrationSerializer(serializers.ModelSerializer):
    is_registered = serializers.SerializerMethodField()

    def get_is_registered(self, obj):
        return False

    class Meta:
        model = Event
        fields = ('pk', 'title', 'image', 'is_registration_open', 'is_registered')


class CollaboratorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('pk', 'first_name', 'last_name', 'email', 'avatar', 'skype_id')


class EventParticipantListSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='num_participants')

    class Meta:
        model = Event
        depth = 1
        fields = ('pk', 'title', 'image', 'count', 'is_registration_open', 'participants')


class EventCollaboratorListSerializer(serializers.ModelSerializer):
    collaborators = CollaboratorSimpleSerializer(many=True)
    count = serializers.IntegerField(source='num_collaborators')

    class Meta:
        model = Event
        depth = 1
        fields = ('pk', 'title', 'image', 'count', 'is_registration_open', 'collaborators')


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant


class AttendanceSerializer(serializers.ModelSerializer):
    event_details = EventSimpleSerializer(source='event')

    class Meta:
        model = Attendance
        depth = 1
        fields = ('pk', 'datetime_register', 'is_registered', 'event_details', 'participant')


class CollaboratorAttendanceSerializer(serializers.ModelSerializer):
    is_registered = serializers.SerializerMethodField('_is_registered')

    def _is_registered(self, obj):
        is_registered_value = self.context.get('is_registered')
        return is_registered_value

    class Meta:
        model = Event
        fields = ('pk',
                  'title',
                  'description',
                  'datetime',
                  'image',
                  'location',
                  'is_registration_open',
                  'is_registered')
