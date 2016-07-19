from .models import Activity
from categories.models import Category
from employees.models import Employee
from rest_framework.test import APITestCase


class ActivityTestCase(APITestCase):
    def setUp(self):
        Category.objects.create(name='Coworker')
        Employee.objects.create_superuser('user1', 'user1@email.com', 'user1password')
        Employee.objects.create_superuser('user2', 'user2@email.com', 'user2password')

    def test_activity_creation(self):
        activity = Activity(text='foobar activity')
        self.assertEqual(activity.text, 'foobar activity')
