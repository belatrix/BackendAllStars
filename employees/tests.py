from .models import Employee
from .serializers import EmployeeSerializer, EmployeeAvatarSerializer, EmployeeListSerializer
from categories.serializers import CategorySerializer
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class EmployeeTestCase(APITestCase):
    def setUp(self):
        Employee.objects.create_superuser('user1', 'user1@email.com', 'user1password')
        Employee.objects.create_superuser('user2', 'user2@email.com', 'user2password')

    def test_employee_creation(self):
        employee1 = Employee.objects.get(email='user1@email.com')
        employee2 = Employee.objects.get(username='user2')
        self.assertEqual(employee1.username, 'user1')
        self.assertEqual(employee2.email, 'user2@email.com')

    def test_employee_list(self):
        response_data = {"count":2,"next":None,"previous":None,"results":[{"pk":1,"username":"user1","email":"user1@email.com","first_name":"","last_name":"","level":0,"avatar":None,"score":0},{"pk":2,"username":"user2","email":"user2@email.com","first_name":"","last_name":"","level":0,"avatar":None,"score":0}]}
        url = reverse('employees:employee_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)