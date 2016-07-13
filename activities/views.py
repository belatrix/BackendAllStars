from .models import Message
from .serializers import MessageSerializer
from constance import config
from employees.models import Employee, EmployeeDevice, Location
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests


def send_message_android(destination, title, message):
    headers = {
        'Authorization': 'key=' + settings.FIREBASE_SERVER_KEY,
        'Content - Type': 'application/json'
    }
    payload = {
        "to": destination,
        "notification": {"title": title, "text": message}
    }
    request = requests.post(
        settings.FIREBASE_API_URL,
        json=payload,
        headers=headers
    )
    print request.text


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
                try:
                    employee_devices = EmployeeDevice.objects.get(username=employee)
                    if employee_devices.android_device:
                        send_message_android(
                            employee_devices.android_device,
                            config.TITLE_PUSH_NOTIFICATION,
                            message.text)
                    if employee_devices.ios_device:
                        # TODO iOS push notification
                        pass
                except:
                    pass
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
                try:
                    employee_devices = EmployeeDevice.objects.get(username=employee)
                    if employee.location == location:
                        if employee_devices.android_device:
                            send_message_android(
                                employee_devices.android_device,
                                config.TITLE_PUSH_NOTIFICATION,
                                message.text)
                        if employee_devices.ios_device:
                            # TODO iOS push notification
                            pass
                except:
                    pass
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            content = {'detail': config.NO_MESSAGE}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
