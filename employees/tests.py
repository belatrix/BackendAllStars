from .models import Employee
from .serializers import EmployeeSerializer, EmployeeAvatarSerializer, EmployeeListSerializer
from categories.serializers import CategorySerializer
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.test import APITestCase, APIClient


class EmployeeTestCase(APITestCase):
    def setUp(self):
        Employee.objects.create_superuser('user', 'user@email.com', 'userpassword')

    def test_employee_creation(self):
        # token = Token.objects.get(user__username='user')
        # user = APIClient()
        # user.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # employee1 = Employee.objects.get(username='user')
        # print user.username
        # #user.login(username=employee1.username, password=employee1.password)
        employee1 = Employee.objects.get(email='user@email.com')
        self.assertEqual(employee1.username, 'user')

    def test_employee_list(self):
        employees = Employee.objects.all()
        paginator = Paginator(employees, 20)
        print paginator.page(1)
        print paginator.page(1).object_list
        serializer = EmployeeListSerializer(employees, many=True)
        url = reverse('employees:employee_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)