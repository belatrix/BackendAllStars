from .models import Category, Keyword
from .serializers import CategorySerializer, CategorySimpleSerializer
from .serializers import KeywordListSerializer, SubcategoryListSerializer
from constance import config
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def category_add(request):
    """
    Add new category
    ---
    serializer: categories.serializers.CategorySimpleSerializer
    responseMessages:
    - code: 400
      message: Bad request.
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'POST':
        serializer = CategorySimpleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        content = {'detail': config.CATEGORY_BAD_REQUEST}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'GET', 'PUT'])
@permission_classes((IsAuthenticated,))
def category_detail(request, category_id):
    """
    Edit category
    ---
    serializer: categories.serializers.CategorySimpleSerializer
    response_serializer: categories.serializers.CategorySerializer
    responseMessages:
    - code: 400
      message: Bad request.
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CategorySimpleSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        content = {'detail': config.CATEGORY_BAD_REQUEST}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.is_active = False
        category.save()
        return Response(status=status.HTTP_202_ACCEPTED)


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
        categories = get_list_or_404(Category, is_active=True)
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
        keywords = get_list_or_404(Keyword, is_active=True)
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
                new_keyword = request.data['name'].upper()
                keyword = Keyword.objects.create(name=new_keyword)
                keyword.save()
                keywords = get_list_or_404(Keyword)
                serializer = KeywordListSerializer(keywords, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                raise NotAcceptable(config.KEYWORD_ALREADY_EXISTS)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def subcategory_add(request):
    """
    Add new subcategory
    ---
    serializer: categories.serializers.SubcategoryListSerializer
    responseMessages:
    - code: 400
      message: Bad request.
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'POST':
        serializer = SubcategoryListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        content = {'detail': config.SUBCATEGORY_BAD_REQUEST}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
