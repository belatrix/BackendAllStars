from .models import Event
from employees.models import Location
from rest_framework.test import APITestCase


class EventTestCase(APITestCase):
    def setUp(self):
        location = Location.objects.create(name='location 1')
        Event.objects.create(name='Event 1', location=location)
        Event.objects.create(name='Event 2', location=location)

    def test_event_creation(self):
        location = Location.objects.get(name='location 1')
        event1 = Event.objects.get(name='Event 1')
        self.assertEqual(event1.name, 'Event 1')
        self.assertEqual(event1.location, location)
