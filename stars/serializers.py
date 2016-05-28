from .models import Star
from categories.serializers import CategorySimpleSerializer, KeywordSerializer
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


class StarBulkSerializer(serializers.Serializer):
    category = serializers.IntegerField()
    subcategory = serializers.IntegerField()
    keyword = serializers.IntegerField()
    text = serializers.CharField()
    to_users = serializers.ListField(
        child=serializers.IntegerField()
    )


class StarSmallSerializer(serializers.ModelSerializer):
    from_user = EmployeeSimpleSerializer()
    category = CategorySimpleSerializer()
    keyword = KeywordSerializer()

    class Meta:
        model = Star
        depth = 1
        fields = ('pk', 'date', 'text', 'category', 'from_user', 'keyword')


class StarSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ('pk', 'category', 'subcategory', 'keyword', 'text')


class StarEmployeesSubcategoriesSerializer(serializers.Serializer):
    pk = serializers.IntegerField(source='subcategory__pk')
    name = serializers.CharField(max_length=100, source='subcategory__name')
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
    avatar = serializers.SerializerMethodField()
    num_stars = serializers.IntegerField()


class StarKeywordList(serializers.Serializer):
    pk = serializers.IntegerField(source='keyword__pk')
    name = serializers.CharField(source='keyword__name')
    num_stars = serializers.IntegerField()
