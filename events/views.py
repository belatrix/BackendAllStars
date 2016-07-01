from .models import Event, Participant
from .serializers import EventSerializer, EventSimpleSerializer, ParticipantSerializer
from constance import config
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, get_list_or_404
from employees.models import Employee
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', ])
def event(request, event_id):
    """
    Returns event details
    ---
    serializer: events.serializers.EventSerializer
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
        try:
            event = Event.objects.annotate(
                num_participants=Count('participants', distinct=True),
                num_collaborators=Count('collaborators', distinct=True)).get(pk=event_id)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(e)


@api_view(['GET', ])
def event_list(request):
    """
    Returns the full events list or result list if you use ?search=
    ---
    serializer: events.serializers.EventSerializer
    parameters:
    - name: search
      required: false
      type: string
      paramType: query
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
        if request.GET.get('search'):
            request_terms = request.GET.get('search')
            search_terms_array = request_terms.split()

            initial_term = search_terms_array[0]
            event_list = Event.objects.annotate(
                num_participants=Count('participants', distinct=True),
                num_collaborators=Count('collaborators', distinct=True)).filter(
                    Q(title__icontains=initial_term) |
                    Q(description__icontains=initial_term))
            if len(search_terms_array) > 1:
                for term in range(1, len(search_terms_array)):
                    event_list = event_list.filter(Q(title__icontains=search_terms_array[term]) |
                                                   Q(description__icontains=search_terms_array[term]))
        else:
            event_list = Event.objects.annotate(
                num_participants=Count('participants', distinct=True),
                num_collaborators=Count('collaborators', distinct=True)).all()
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(event_list, request)
        serializer = EventSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def event_register_collaborator(request, event_id, employee_id):
    """
    Register participant into event
    ---
    response_serializer: events.serializers.EventSimpleSerializer
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
    if request.method == 'PUT':
        event = get_object_or_404(Event, pk=event_id)
        collaborator = get_object_or_404(Employee, pk=employee_id)
        event.collaborators.add(collaborator)
        event.save()
        serializer = EventSimpleSerializer(event)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['PUT', ])
def event_register_participant(request, event_id, participant_id):
    """
    Register participant into event
    ---
    response_serializer: events.serializers.EventSimpleSerializer
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
    if request.method == 'PUT':
        event = get_object_or_404(Event, pk=event_id)
        participant = get_object_or_404(Participant, pk=participant_id)
        event.participants.add(participant)
        event.save()
        serializer = EventSimpleSerializer(event)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def event_unregister_collaborator(request, event_id, employee_id):
    """
    Unregister participant into event
    ---
    response_serializer: events.serializers.EventSimpleSerializer
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
    if request.method == 'PUT':
        event = get_object_or_404(Event, pk=event_id)
        collaborator = get_object_or_404(Employee, pk=employee_id)
        event.collaborators.remove(collaborator)
        event.save()
        serializer = EventSimpleSerializer(event)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['PUT', ])
def event_unregister_participant(request, event_id, participant_id):
    """
    Unregister participant into event
    ---
    response_serializer: events.serializers.EventSimpleSerializer
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
    if request.method == 'PUT':
        event = get_object_or_404(Event, pk=event_id)
        participant = get_object_or_404(Participant, pk=participant_id)
        event.participants.remove(participant)
        event.save()
        serializer = EventSimpleSerializer(event)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
def participant(request, participant_id):
    """
    Returns participant details
    ---
    response_serializer: events.serializers.ParticipantSerializer
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
        participant = get_object_or_404(Participant, pk=participant_id)
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def participant_create(request):
    """
    Creates a participant
    ---
    serializer: events.serializers.ParticipantSerializer
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
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            content = {'detail': config.PARTICIPANT_ALREADY_REGISTERED_OR_BAD_REQUEST}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def participant_list(request):
    """
    Returns the full participant list or result list if you use ?search=
    ---
    serializer: events.serializers.ParticipantSerializer
    parameters:
    - name: search
      required: false
      type: string
      paramType: query
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        if request.GET.get('search'):
            request_terms = request.GET.get('search')
            search_terms_array = request_terms.split()

            initial_term = search_terms_array[0]
            participant_list = Participant.objects.filter(
                Q(fullname__icontains=initial_term) |
                Q(email__icontains=initial_term))

            if len(search_terms_array) > 1:
                for term in range(1, len(search_terms_array)):
                    participant_list = participant_list.filter(Q(fullname__icontains=search_terms_array[term]) |
                                                               Q(email__icontains=search_terms_array[term]))
        else:
            participant_list = get_list_or_404(Participant)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(participant_list, request)
        serializer = ParticipantSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
