from .models import Star
from rest_framework import serializers


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ('date', 'text', 'from_user', 'to_user', 'category', 'subcategory')