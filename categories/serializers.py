from .models import Category, Subcategory
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name', 'weight', 'comment_required')


class SubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('pk', 'name')


class SubcategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        depth = 1
        fields = ('pk', 'name', 'category')
