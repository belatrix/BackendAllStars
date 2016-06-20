from .models import Event
from .serializers import EventSerializer, EventListSerializer
from django.db.models import Count, Q
from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
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
@permission_classes((IsAuthenticated,))
def event_list(request):
    """
    Returns the full events list or result list if you use ?search=
    ---
    serializer: events.serializers.EventListSerializer
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
            elem_list = Event.objects.filter(Q(title__icontains=initial_term) |
                                             Q(description__icontains=initial_term))
            if len(search_terms_array) > 1:
                for term in range(1, len(search_terms_array)):
                    elem_list = elem_list.filter(Q(title__icontains=search_terms_array[term]) |
                                                 Q(description__icontains=search_terms_array[term]))
        else:
            elem_list = get_list_or_404(Event)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(elem_list, request)
        serializer = EventListSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
