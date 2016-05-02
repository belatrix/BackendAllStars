from .models import Employee
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        depth = 1
        fields = ('pk',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'role',
                  'skype_id',
                  'avatar',
                  'last_month_score',
                  'last_year_score',
                  'current_month_score',
                  'current_year_score',
                  'level',
                  'total_score',
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
                  'total_score',
                  'last_month_score',
                  'last_year_score',
                  'current_month_score',
                  'current_year_score')


class EmployeeTopTotalScoreList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='total_score')

    class Meta:
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeTopLevelList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='level')

    class Meta:
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeTopCurrentMonthList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='current_month_score')

    class Meta:
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeTopCurrentYearList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='current_year_score')

    class Meta:
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeTopLastMonthList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='last_month_score')

    class Meta:
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeTopLastYearList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='last_year_score')

    class Meta:
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('pk', 'avatar')


class EmployeeAuthenticationResponse(serializers.Serializer):
    token = serializers.CharField(max_length=40)
    user_id = serializers.IntegerField()
