from .models import Category, Keyword
from rest_framework import serializers


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('pk', 'name')


class KeywordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('pk', 'name')


class SubcategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Subcategory
        depth = 1
        fields = ('pk', 'name', 'category')


class SubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Subcategory
        fields = ('pk', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name', 'weight', 'comment_required')


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name', 'weight', 'comment_required')
