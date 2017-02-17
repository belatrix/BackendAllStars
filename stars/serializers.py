from .models import EmployeeBadge, Star, Badge
from categories.serializers import CategorySerializer, KeywordSerializer
from employees.models import Employee, Position
from rest_framework import serializers


class PositionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Position


class EmployeeSimpleSerializer(serializers.ModelSerializer):
    position = PositionSerializer()

    class Meta(object):
        model = Employee
        fields = ('pk', 'username', 'first_name', 'last_name', 'avatar', 'position')


class StarSerializer(serializers.ModelSerializer):
    from_user = EmployeeSimpleSerializer()
    keyword = KeywordSerializer()

    class Meta(object):
        model = Star
        fields = ('pk', 'date', 'text', 'from_user', 'to_user', 'category', 'keyword')


class StarInputSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Star
        fields = ('pk', 'date', 'text', 'from_user', 'to_user', 'category', 'keyword')


class StarBulkSerializer(serializers.Serializer):
    category = serializers.IntegerField()
    keyword = serializers.IntegerField()
    text = serializers.CharField()
    to_users = serializers.ListField(
        child=serializers.IntegerField()
    )


class StarSmallSerializer(serializers.ModelSerializer):
    from_user = EmployeeSimpleSerializer()
    category = CategorySerializer()
    keyword = KeywordSerializer()

    class Meta(object):
        model = Star
        depth = 1
        fields = ('pk', 'date', 'text', 'category', 'from_user', 'keyword')


class StarSwaggerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Star
        fields = ('pk', 'category', 'keyword', 'text')


class StarEmployeeCategoriesSerializer(serializers.Serializer):
    pk = serializers.IntegerField(source='category__pk')
    name = serializers.CharField(max_length=100, source='category__name')
    num_stars = serializers.IntegerField()


class StarEmployeeKeywordsSerializer(serializers.Serializer):
    pk = serializers.IntegerField(source='keyword__pk')
    name = serializers.CharField(max_length=100, source='keyword__name')
    num_stars = serializers.IntegerField()


class StarTopEmployeeLists(serializers.Serializer):

    def get_avatar(self, data):
        employee = Employee.objects.get(pk=data['to_user__pk'])
        if employee.avatar:
            avatar_url = employee.avatar.url
        else:
            avatar_url = ""
        return avatar_url

    pk = serializers.IntegerField(source='to_user__pk')
    username = serializers.CharField(max_length=100, source='to_user__username')
    first_name = serializers.CharField(max_length=100, source='to_user__first_name')
    last_name = serializers.CharField(max_length=100, source='to_user__last_name')
    level = serializers.IntegerField(source='to_user__level')
    avatar = serializers.SerializerMethodField()
    num_stars = serializers.IntegerField()


class StarKeywordList(serializers.Serializer):
    pk = serializers.IntegerField(source='keyword__pk')
    name = serializers.CharField(source='keyword__name')
    num_stars = serializers.IntegerField()


class BadgeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Badge
        fields = ('pk', 'name', 'icon', 'description')


class EmployeeBadgeSerializer(serializers.ModelSerializer):
    to_user = EmployeeSimpleSerializer()
    assigned_by = EmployeeSimpleSerializer()
    badge = BadgeSerializer()

    class Meta(object):
        model = EmployeeBadge
        fields = ('pk', 'date', 'to_user', 'assigned_by', 'badge')


class EmployeeBadgeListSerializer(serializers.Serializer):
    pk = serializers.IntegerField(source='badge__pk')
    name = serializers.CharField(source='badge__name')
    num_employees = serializers.IntegerField()


class EmployeeGroupedListSerializer(serializers.Serializer):

    def get_avatar(self, data):
        employee = Employee.objects.get(pk=data['to_user__pk'])
        if employee.avatar:
            avatar_url = employee.avatar.url
        else:
            avatar_url = ""
        return avatar_url

    pk = serializers.IntegerField(source='to_user__pk')
    username = serializers.CharField(max_length=100, source='to_user__username')
    first_name = serializers.CharField(max_length=100, source='to_user__first_name')
    last_name = serializers.CharField(max_length=100, source='to_user__last_name')
    level = serializers.IntegerField(source='to_user__level')
    avatar = serializers.SerializerMethodField()
