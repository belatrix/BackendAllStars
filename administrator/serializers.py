from categories.models import Category, Keyword, Subcategory
from rest_framework import serializers


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name')


class SubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('pk', 'name')


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategoryListSerializer(many=True, source='subcategory_set')

    class Meta:
        model = Category
        fields = ('pk', 'name', 'weight', 'is_active', 'comment_required', 'subcategories')


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword


class SubcategorySimpleSerializer(serializers.ModelSerializer):
    categories = CategoryListSerializer(many=True, source='category')

    class Meta:
        model = Subcategory
        fields = ('pk', 'name', 'is_active', 'categories')


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('pk', 'name', 'is_active')


class CategoryPKListSerializer(serializers.Serializer):
    categories = serializers.ListField(
        child=serializers.IntegerField()
    )


class SubcategoryPKListSerializer(serializers.Serializer):
    subcategories = serializers.ListField(
        child=serializers.IntegerField()
    )
