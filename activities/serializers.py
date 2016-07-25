from .models import Message, Activity
from employees.models import Employee
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):

    def get_avatar(self, data):
        employee = Employee.objects.get(pk=data.from_user.pk)
        if employee.avatar:
            avatar_url = employee.avatar.url
        else:
            avatar_url = ""
        return avatar_url

    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'datetime', 'text', 'to_user', 'from_user', 'avatar')


class ActivitySerializer(serializers.ModelSerializer):

    def get_avatar(self, data):
        employee = Employee.objects.get(pk=data.to_user.pk)
        if employee.avatar:
            avatar_url = employee.avatar.url
        else:
            avatar_url = ""
        return avatar_url

    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ('id', 'datetime', 'text', 'to_user', 'avatar')


class NotificationSerializer(serializers.Serializer):

    def get_avatar(self, data):
        employee = Employee.objects.get(pk=data['profile'])
        if employee.avatar:
            avatar_url = employee.avatar.url
        else:
            avatar_url = ""
        return avatar_url

    datetime = serializers.DateTimeField()
    text = serializers.CharField()
    avatar = serializers.SerializerMethodField()
