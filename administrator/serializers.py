from activities.models import Message
from categories.models import Category, Keyword
from employees.models import Employee, Position, Role, Location
from events.models import Event, EventActivity
from stars.models import Badge
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Category


class KeywordSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Keyword


class BadgeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Badge


class PositionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Position


class RoleSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Role


class LocationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Location


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Employee
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'avatar')


class EmployeeTopSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Employee
        fields = ('pk',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'avatar',
                  'current_month_score',
                  'current_year_score',
                  'last_month_score',
                  'last_year_score',
                  'total_score',
                  'level')


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True)

    class Meta(object):
        model = Event


class EventActivitySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EventActivity


class MessageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Message

class SiteInfoSerializer(serializers.Serializer):
    site = serializers.CharField(max_length=100)
    email_domain = serializers.CharField(max_length=100)
    backend_version = serializers.CharField(max_length=100)
