from .models import Event, EventParticipant
from .serializers import EventSerializer
from employees.models import Employee
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework. permissions import IsAuthenticated


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
