from .models import Category
from .serializers import CategorySerializer
from employees.models import Employee
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CategoryTestCase(APITestCase):
    def setUp(self):
        Category.objects.create(name='Coworker')
        Employee.objects.create_superuser('user1', 'user1@email.com', 'user1password')
        Category.objects.create(name='Category1', weight=2)
        Category.objects.create(name='Category2')
        self.client.login(username='user1', password='user1password')

    def test_category_creation(self):
        category1 = Category.objects.get(name='Category1')
        category2 = Category.objects.get(name='Category2')
        self.assertEqual(category1.weight, 2)
        self.assertEqual(category2.weight, 1)

    def test_category_list(self):
        categories = Category.objects.all()
        response_data = CategorySerializer(categories, many=True).data
        url = reverse('categories:category_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
