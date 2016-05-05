from .models import Star
from employees.models import Employee
from rest_framework import serializers


class EmployeeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar')


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ('pk', 'date', 'text', 'from_user', 'to_user', 'category', 'subcategory', 'keyword')


class StarSmallSerializer(serializers.ModelSerializer):
    from_user = EmployeeSimpleSerializer()

    class Meta:
        model = Star
        depth = 1
        fields = ('pk', 'date', 'text', 'category', 'from_user')


class StarSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ('pk', 'category', 'subcategory', 'keyword', 'text')


class StarEmployeesSubcategoriesSerializer(serializers.Serializer):
    pk = serializers.IntegerField(source='subcategory__pk')
    name = serializers.CharField(max_length=100, source='subcategory__name')
    num_stars = serializers.IntegerField()


class StarTopEmployeeLists(serializers.Serializer):
    pk = serializers.IntegerField(source='to_user__id')
    username = serializers.CharField(max_length=100, source='to_user__username')
    first_name = serializers.CharField(max_length=100, source='to_user__first_name')
    last_name = serializers.CharField(max_length=100, source='to_user__last_name')
    num_stars = serializers.IntegerField()
