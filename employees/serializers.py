from .models import Employee, Location, Role, EmployeeDevice, Position
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Location
        fields = ('pk', 'name', 'icon', 'is_active')


class EmployeeRoleListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Role
        fields = ('pk', 'name')


class EmployeePositionListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Position


class EmployeeSerializer(serializers.ModelSerializer):
    is_admin = serializers.CharField(source='is_staff')
    roles = EmployeeRoleListSerializer(source='role', many=True)

    class Meta(object):
        model = Employee
        depth = 1
        fields = ('pk',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'location',
                  'emergency_phone_contact',
                  'skype_id',
                  'avatar',
                  'is_base_profile_complete',
                  'is_password_reset_required',
                  'last_month_score',
                  'last_year_score',
                  'current_month_score',
                  'current_year_score',
                  'level',
                  'total_score',
                  'is_active',
                  'is_blocked',
                  'is_admin',
                  'last_login',
                  'total_given',
                  'position',
                  'roles')


class EmployeeCreationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)


class EmployeeCreationListSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20)
    emails = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )


class EmployeeSetListSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=100)
    set_id_list = serializers.ListField(
        child=serializers.IntegerField()
    )


class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Employee
        depth = 1
        fields = ('pk',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'location',
                  'emergency_phone_contact',
                  'level',
                  'avatar',
                  'total_score',
                  'is_blocked',
                  'last_month_score',
                  'last_year_score',
                  'current_month_score',
                  'current_year_score')


class EmployeeLocationListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Location
        fields = ('pk', 'name', 'icon')


class EmployeeTopListSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    avatar = serializers.CharField()
    value = serializers.IntegerField()


class EmployeeTopTotalScoreList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='total_score')

    class Meta(object):
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeTopLevelList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='level')

    class Meta(object):
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeTopCurrentMonthList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='current_month_score')

    class Meta(object):
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeTopCurrentYearList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='current_year_score')

    class Meta(object):
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeTopLastMonthList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='last_month_score')

    class Meta(object):
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeTopLastYearList(serializers.ModelSerializer):
    value = serializers.IntegerField(source='last_year_score')

    class Meta(object):
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'value')


class EmployeeAvatarSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Employee
        fields = ('pk', 'avatar')


class EmployeeAuthenticationResponse(serializers.Serializer):
    token = serializers.CharField(max_length=40)
    user_id = serializers.IntegerField()


class EmployeeDeviceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EmployeeDevice
        fields = ('username', 'android_device', 'ios_device')
