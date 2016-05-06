from .models import Employee
from rest_framework.test import APITestCase


class EmployeeTestCase(APITestCase):
    def setUp(self):
        Employee.objects.create_superuser('user1', 'user1@email.com', 'user1password')
        Employee.objects.create_superuser('user2', 'user2@email.com', 'user2password')

    def test_employee_creation_without_endpoint(self):
        employee1 = Employee.objects.get(email='user1@email.com')
        employee2 = Employee.objects.get(username='user2')
        self.assertEqual(employee1.username, 'user1')
        self.assertEqual(employee2.email, 'user2@email.com')
