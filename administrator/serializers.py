from categories.models import Category, Keyword
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
