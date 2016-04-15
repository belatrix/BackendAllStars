from .models import Employee
from .serializers import EmployeeSerializer, EmployeeListSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', ])
def employee_list(request):
    if request.method == 'GET':
        employee_list = get_list_or_404(Employee)
        paginator = PageNumberPagination()
        paginator.page_size=1
        results = paginator.paginate_queryset(employee_list, request)
        serializer = EmployeeListSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['GET', ])
def employee(request, employee_id):
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', ])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def top(request, kind, quantity):
    try:
        if request.method == 'GET':
            employee_list = Employee.objects.order_by('-'+kind)[:quantity]
            serializer = EmployeeListSerializer(employee_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        raise APIException(e)


@api_view(['GET', ])
def search(request, search_term):
    if request.method == 'GET':
        employee_list = Employee.objects.filter(
            Q(first_name__icontains=search_term)|
            Q(last_name__icontains=search_term)|
            Q(username__icontains=search_term))
        paginator = PageNumberPagination()
        paginator.page_size=20
        results = paginator.paginate_queryset(employee_list, request)
        serializer = EmployeeListSerializer(results, many=True)
        return  paginator.get_paginated_response(serializer.data)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})