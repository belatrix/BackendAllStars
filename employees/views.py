from .models import Employee
from .serializers import EmployeeSerializer, EmployeeListSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', ])
def employee_list(request):
    if request.method == 'GET':
        employee_list = Employee.objects.all()
        serializer = EmployeeListSerializer(employee_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', ])
def employee(request, employee_id):
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)