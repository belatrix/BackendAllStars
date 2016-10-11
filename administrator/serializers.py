from categories.models import Category, Keyword, Subcategory
from rest_framework import serializers


class SubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('pk', 'name')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategoryListSerializer(many=True, source='subcategory_set')

    class Meta:
        model = Category
        fields = ('pk', 'name', 'weight', 'is_active', 'comment_required', 'subcategories')


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('pk', 'name', 'is_active')
