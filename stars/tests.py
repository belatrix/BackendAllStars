from .models import Star
from categories.models import Category, Keyword
from employees.models import Employee
from rest_framework.test import APITestCase


class ActivityTestCase(APITestCase):
    def setUp(self):
        Category.objects.create(name='Coworker')
        Keyword.objects.create(name='foobar')
        Employee.objects.create_superuser('user1', 'user1@email.com', 'user1password')
        Employee.objects.create_superuser('user2', 'user2@email.com', 'user2password')

    def test_star_creation(self):
        employee1 = Employee.objects.get(username='user1')
        employee2 = Employee.objects.get(username='user2')
        category1 = Category.objects.get(name='Coworker')
        keyword1 = Keyword.objects.get(name='foobar')
        star = Star(
            text='foobar',
            from_user=employee1,
            to_user=employee2,
            category=category1,
            keyword=keyword1)
        self.assertEqual(star.text, 'foobar')
