from .models import Category, Keyword
from .serializers import CategorySerializer
from .serializers import KeywordSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def category_detail(request, category_id):
    """
    Category detail
    ---
    serializer: categories.serializers.CategorySerializer
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


@api_view(['GET', ])
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
    serializer: categories.serializers.KeywordSerializer
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
        serializer = KeywordSerializer(keywords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def keyword_detail(request, keyword_id):
    """
    Keyword detail
    ---
    serializer: categories.serializers.KeywordSerializer
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
    keyword = get_object_or_404(Keyword, pk=keyword_id)
    if request.method == 'GET':
        serializer = KeywordSerializer(keyword)
        return Response(serializer.data, status=status.HTTP_200_OK)
