from categories.models import Category, Keyword
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
