from .models import Activity, Message
from .serializers import ActivitySerializer, MessageSerializer, NotificationSerializer
from constance import config
from employees.models import Employee, Location
from django.db.models import Q
from django.shortcuts import get_object_or_404
from itertools import chain
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.send_messages import evaluate_user_permissions_for_push, send_push_notification


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def send_message_all(request):
    """
    Send message to all employees
    ---
    response_serializer: employees.serializers.EmployeeDeviceSerializer
    parameters:
    - name: message
      type: string
      required: true
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if evaluate_user_permissions_for_push(request.user):
        if request.method == 'POST':
            if 'message' in request.data:
                employee_list = Employee.objects.all()
                message = Message(
                    text=request.data['message'],
                    from_user=request.user,
                    to_user="all")
                message.save()
                for employee in employee_list:
                    send_push_notification(employee, message.text)
                serializer = MessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                content = {'detail': config.NO_MESSAGE}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'detail': config.NO_ALLOWED_TO_SEND_MESSAGE}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def send_message_to(request, employee_username):
    """
    Send message to employee
    ---
    response_serializer: employees.serializers.EmployeeDeviceSerializer
    parameters:
    - name: message
      type: string
      required: true
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if evaluate_user_permissions_for_push(request.user):
        if request.method == 'POST':
            if 'message' in request.data:
                employee = get_object_or_404(Employee, username=employee_username)
                message = Message(
                    text=request.data['message'],
                    from_user=request.user,
                    to_user=employee.username
                )
                message.save()
                send_push_notification(employee, message.text)
                serializer = MessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                content = {'detail': config.NO_MESSAGE}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'detail': config.NO_ALLOWED_TO_SEND_MESSAGE}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def send_message_location(request, location_id):
    """
    Send message to all employees by location
    ---
    response_serializer: employees.serializers.EmployeeDeviceSerializer
    parameters:
    - name: message
      type: string
      required: true
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if evaluate_user_permissions_for_push(request.user):
        if request.method == 'POST':
            if 'message' in request.data:
                employee_list = Employee.objects.all()
                location = get_object_or_404(Location, pk=location_id)
                message = Message(
                    text=request.data['message'],
                    from_user=request.user,
                    to_user="location: " + location.name)
                message.save()
                for employee in employee_list:
                    if employee.location == location:
                        send_push_notification(employee, message.text)
                serializer = MessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                content = {'detail': config.NO_MESSAGE}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
        content = {'detail': config.NO_ALLOWED_TO_SEND_MESSAGE}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_messages(request, employee_id):
    """
    Get all messages for employee id
    ---
    response_serializer: activities.serializers.MessageSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        messages = Message.objects.filter(Q(to_user='all') | Q(to_user=employee.location.name) | Q(to_user=employee.username))
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_messages_from(request, employee_id):
    """
    Get all messages sent from employee id
    ---
    response_serializer: activities.serializers.MessageSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        messages = Message.objects.filter(from_user=employee)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_messages_from_all(request):
    """
    Get all messages sent
    ---
    response_serializer: activities.serializers.MessageSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if request.method == 'GET':
        messages = Message.objects.all()
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_activities(request, employee_id):
    """
    Get all activities for employee id
    ---
    response_serializer: activities.serializers.ActivitySerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        activities = Activity.objects.filter(to_user=employee)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(activities, request)
        serializer = ActivitySerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_notifications(request, employee_id):
    """
    Get all notifications for employee id
    ---
    response_serializer: activities.serializers.NotificationSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        activities = Activity.objects.filter(to_user=employee).defer("datetime", "text")
        messages = Message.objects.filter(
            Q(to_user='all') |
            Q(to_user=employee.location.name) |
            Q(to_user=employee.username)).defer("datetime", "text")
        notifications = list(chain(activities, messages))
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
