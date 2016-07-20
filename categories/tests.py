from .models import Category, Subcategory
from .serializers import CategorySerializer, SubcategoryDetailSerializer, SubcategoryListSerializer
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
        Subcategory.objects.create(name='Subcategory1')
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

    def test_subcategory_list_by_category(self):
        category1 = Category.objects.get(name='Category1')
        subcategory1 = Subcategory.objects.get(name='Subcategory1')
        subcategory1.category.add(category1)
        subcategories = Subcategory.objects.filter(category=category1)
        response_data = SubcategoryListSerializer(subcategories, many=True).data
        url = reverse('categories:subcategory_list_by_category', args=[category1.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subcategory_list(self):
        subcategories = Subcategory.objects.all()
        response_data = SubcategoryListSerializer(subcategories, many=True).data
        url = reverse('categories:subcategory_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subcategory_detail(self):
        category1 = Category.objects.get(name='Category1')
        subcategory1 = Subcategory.objects.get(name='Subcategory1')
        subcategory1.category.add(category1)
        subcategory = Subcategory.objects.get(pk=subcategory1.id)
        response_data = SubcategoryDetailSerializer(subcategory).data
        url = reverse('categories:subcategory_detail', args=[subcategory1.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
