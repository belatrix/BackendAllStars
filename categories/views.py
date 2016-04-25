from .models import Category, Subcategory
from .serializers import CategorySerializer, SubCategoryListSerializer, SubcategoryDetailSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def subcategories_list(request, category_id):
    if request.method == 'GET':
        subcategories = Subcategory.objects.filter(category=category_id)
        serializer = SubCategoryListSerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = get_list_or_404(Category)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def subcategory_detail(request, subcategory_id):
    if request.method == 'GET':
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        serializer = SubcategoryDetailSerializer(subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)
