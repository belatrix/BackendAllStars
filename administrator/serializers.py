from categories.models import Category, Keyword
from employees.models import Position, Role, Location
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
