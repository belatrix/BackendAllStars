from .models import Star
from employees.models import Employee
from rest_framework import serializers


class EmployeeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name')


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ('pk', 'date', 'text', 'from_user', 'to_user', 'category', 'subcategory')


class StarSmallSerializer(serializers.ModelSerializer):
    from_user = EmployeeSimpleSerializer()

    class Meta:
        model = Star
        depth = 1
        fields = ('pk', 'date', 'text', 'category', 'from_user')


class StarSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ('pk', 'category', 'subcategory', 'text')


class StarEmployeesSubcategoriesSerializer(serializers.Serializer):
    subcategory__pk = serializers.IntegerField()
    subcategory__name = serializers.CharField(max_length=100)
    num_stars = serializers.IntegerField()


class StarTopEmployeeLists(serializers.Serializer):
    to_user__id = serializers.IntegerField()
    to_user__username = serializers.CharField(max_length=100)
    to_user__first_name = serializers.CharField(max_length=100)
    to_user__last_name = serializers.CharField(max_length=100)
    num_stars = serializers.IntegerField()
