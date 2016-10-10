from categories.models import Category, Keyword, Subcategory
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        depth = 1
