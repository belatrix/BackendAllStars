from .models import Category, Keyword, Subcategory
from .serializers import CategorySerializer, KeywordListSerializer, SubcategoryListSerializer, SubcategoryDetailSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def category_list(request):
    """
    Returns full category list ordered by weight
    ---
    serializer: categories.serializers.CategorySerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        categories = get_list_or_404(Category)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def keyword_list(request):
    """
    Returns full keyword list ordered by name
    ---
    serializer: categories.serializers.KeywordListSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        keywords = get_list_or_404(Keyword)
        serializer = KeywordListSerializer(keywords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def subcategory_detail(request, subcategory_id):
    """
    Returns subcategory detail category list
    ---
    serializer: categories.serializers.SubcategoryDetailSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        serializer = SubcategoryDetailSerializer(subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def subcategory_list(request):
    """
    Returns full subcategory list ordered by name
    ---
    serializer: categories.serializers.SubcategoryListSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        subcategories = get_list_or_404(Subcategory)
        serializer = SubcategoryListSerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def subcategory_list_by_category(request, category_id):
    """
    Returns full subcategory list according to category id
    ---
    serializer: categories.serializers.SubcategoryListSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        subcategories = Subcategory.objects.filter(category=category_id)
        serializer = SubcategoryListSerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)