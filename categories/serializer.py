from .models import Subcategory
from rest_framework import serializers

class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('pk',
                  'name')
