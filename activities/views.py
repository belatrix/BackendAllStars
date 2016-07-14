from .models import Message
from .serializers import MessageSerializer
from constance import config
from employees.models import Employee, EmployeeDevice, Location
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.send_messages import send_push_notification


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
