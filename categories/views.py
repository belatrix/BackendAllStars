from .models import Category, Keyword, Subcategory
from .serializers import CategorySerializer, KeywordListSerializer, SubcategoryListSerializer, SubcategoryDetailSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def category_list(request):
    """
    Returns full category list ordered by weight
    ---
    serializer: categories.serializers.CategorySerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        categories = get_list_or_404(Category)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def keyword_list(request):
    """
    Returns full keyword list ordered by name
    ---
    serializer: categories.serializers.KeywordListSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        keywords = get_list_or_404(Keyword)
        serializer = KeywordListSerializer(keywords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def keyword_add(request):
    """
    Add keyword
    ---
    response_serializer: categories.serializers.KeywordListSerializer
    parameters:
    - name: name
      type: string
      required: true
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if request.method == 'POST':
        if 'name' in request.data:
            try:
                new_keyword = request.data['name'].title()
                keyword = Keyword.objects.create(name=new_keyword)
                keyword.save()
                keywords = get_list_or_404(Keyword)
                serializer = KeywordListSerializer(keywords, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                raise APIException(e)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def subcategory_detail(request, subcategory_id):
    """
    Returns subcategory detail category list
    ---
    serializer: categories.serializers.SubcategoryDetailSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        serializer = SubcategoryDetailSerializer(subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def subcategory_list(request):
    """
    Returns full subcategory list ordered by name
    ---
    serializer: categories.serializers.SubcategoryListSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        subcategories = get_list_or_404(Subcategory)
        serializer = SubcategoryListSerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def subcategory_list_by_category(request, category_id):
    """
    Returns full subcategory list according to category id
    ---
    serializer: categories.serializers.SubcategoryListSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        subcategories = Subcategory.objects.filter(category=category_id)
        serializer = SubcategoryListSerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
