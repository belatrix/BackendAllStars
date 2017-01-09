from .models import Category, Keyword
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Category
        fields = ('pk', 'name', 'comment_required')


class KeywordSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Keyword
        fields = ('pk', 'name')
