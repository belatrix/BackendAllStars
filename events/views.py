from .models import Event, EventParticipant, EventActivity
from .serializers import EventSerializer, EventSimpleSerializer
from .serializers import EventActivitySerializer
from employees.models import Employee
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework. permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def my_upcoming_events(request, employee_id):
    """
    Returns the full upcoming events list for employee
    ---
    serializer: events.serializers.EventSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    events = []
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        records = EventParticipant.objects.filter(participant=employee)

        for record in records:
            event = Event.objects.get(pk=record.event.id)
            if event.is_active and event.is_upcoming:
                events.append(event)

        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def local_events(request, employee_id):
    """
    Returns the full upcoming events list for employee location
    ---
    serializer: events.serializers.EventSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        events = Event.objects.filter(location=employee.location, is_active=True, is_upcoming=True)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def other_location_events(request, employee_id):
    """
    Returns the full upcoming events list for employee location
    ---
    serializer: events.serializers.EventSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    events = []
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        events_list = Event.objects.filter(is_active=True, is_upcoming=True)

        for event in events_list:
            if event.location != employee.location:
                events.append(event)

        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def event_detail(request, employee_id, event_id):
    """
    Return event detail according employee perspective
    ---
    serializer: events.serializers.EventSimpleSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        event = get_object_or_404(Event, pk=event_id)
        employee_registered = EventParticipant.objects.filter(event=event, participant=employee)

        if employee_registered:
            is_registered = True
        else:
            is_registered = False

        data = {"pk": event.id,
                "name": event.name,
                "image": event.image,
                "datetime": event.datetime,
                "address": event.address,
                "description": event.description,
                "is_registered": is_registered}

        serializer = EventSimpleSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
def employee_event_registration(request, employee_id, event_id, action):
    """
    Register / unregister employee to event, action could be true or false
    ---
    response_serializer: employees.serializers.EmployeeSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'PATCH':
        employee = get_object_or_404(Employee, pk=employee_id)
        event = get_object_or_404(Event, pk=event_id)

        employee_registration = EventParticipant.objects.filter(event=event, participant=employee)
        is_registered = False

        if employee_registration:
            if action == 'true':
                is_registered = True
            elif action == 'false':
                employee_registration.delete()
                is_registered = False
            else:
                pass
        else:
            if action == 'true':
                EventParticipant.objects.create(event=event, participant=employee)
                is_registered = True
            else:
                pass

        data = {"pk": event.id,
                "name": event.name,
                "image": event.image,
                "datetime": event.datetime,
                "address": event.address,
                "description": event.description,
                "is_registered": is_registered}

        serializer = EventSimpleSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def event_activities(request, event_id):
    if request.method == 'GET':
        event = get_object_or_404(Event, pk=event_id)
        activities = EventActivity.objects.filter(event=event)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(activities, request)
        serializer = EventActivitySerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
