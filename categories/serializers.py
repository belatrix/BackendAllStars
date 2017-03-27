from .models import Category, Keyword
from constance import config
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Category
        fields = ('pk', 'name', 'comment_required')


class KeywordSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['name'] != data['name'].replace(" ", "").lower():
            raise serializers.ValidationError(config.KEYWORD_NOT_ALLOWED)
        return data

    class Meta(object):
        model = Keyword
        fields = ('pk', 'name')
