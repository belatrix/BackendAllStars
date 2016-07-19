from .models import Event
from categories.models import Category
from employees.models import Employee
from rest_framework.test import APITestCase


class ActivityTestCase(APITestCase):
    def setUp(self):
        Category.objects.create(name='Coworker')
        Employee.objects.create_superuser('user1', 'user1@email.com', 'user1password')
        Employee.objects.create_superuser('user2', 'user2@email.com', 'user2password')

    def test_event_creation(self):
        event = Event(title='foobar')
        self.assertEqual(event.title, 'foobar')

    def test_event_registration_default(self):
        event = Event(title='foobar event')
        self.assertEqual(event.is_registration_open, True)
