from .models import Employee
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('pk',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'role',
                  'skype_id',
                  'last_month_score',
                  'current_month_score',
                  'level',
                  'score',
                  'is_active',
                  'last_login')


class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('pk',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'level',
                  'avatar',
                  'score')

class EmployeeAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('pk', 'avatar')
