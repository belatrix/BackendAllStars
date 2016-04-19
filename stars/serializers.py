from .models import Star
from rest_framework import serializers


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ('date', 'text', 'from_user', 'to_user', 'category', 'subcategory')


class StarSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ('category', 'subcategory', 'text')


class StarEmployeesSubcategoriesSerializer(serializers.Serializer):
    subcategory__pk = serializers.IntegerField()
    subcategory__name = serializers.CharField(max_length=100)
    num_stars = serializers.IntegerField()