from categories.models import Category, Keyword, Subcategory
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CategorySimpleSerializer, CategorySerializer, CategoryPKListSerializer
from .serializers import KeywordSerializer, SubcategorySerializer, SubcategorySimpleSerializer
from .serializers import SubcategoryPKListSerializer


class CategoryList(APIView):
    def get(self, request, format=None):
        """
        List all categories
        """
        categories = get_list_or_404(Category)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create new category
        ---
        serializer: administrator.serializers.CategorySimpleSerializer
        """
        serializer = CategorySimpleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    def get(self, request, category_id, format=None):
        """
        Get category details
        """
        category = get_object_or_404(Category, pk=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, category_id, format=None):
        """
        Edit category
        ---
        serializer: administrator.serializers.CategorySimpleSerializer
        """
        category = get_object_or_404(Category, pk=category_id)
        serializer = CategorySimpleSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, category_id, format=None):
        """
        Assign subcategories to categories
        ---
        parameters:
        - name: body
          required: true
          paramType: body
          pytype: administrator.serializers.SubcategoryPKListSerializer
        """
        category = get_object_or_404(Category, pk=category_id)
        serializer = SubcategoryPKListSerializer(data=request.data)
        if serializer.is_valid():
            subcategory_list = request.data['subcategories']
            CategoryRelationship = Subcategory.category.through
            category_relations = CategoryRelationship.objects.filter(category=category_id)

            # Clean category relationships
            for category_relation in category_relations:
                category_relation.delete()

            # Add category to subcategories
            for subcategory_id in subcategory_list:
                subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
                subcategory.category.add(category)
                subcategory.save()

            response_serializer = CategorySerializer(category)
            return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id, format=None):
        """
        Delete category (inactive category, you should edit is_active attribute to revert this change)
        ---
        serializer: administrator.serializers.CategorySerializer
        """
        category = get_object_or_404(Category, pk=category_id)
        category.is_active = False
        category.save()
        serializer = CategorySimpleSerializer(category)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class KeywordList(APIView):
    def get(self, request, format=None):
        """
        List all keywords (tags, skills)
        """
        keywords = get_list_or_404(Keyword)
        serializer = KeywordSerializer(keywords, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create new keyword (tag, skill)
        ---
        serializer: administrator.serializers.KeywordSerializer
        """
        serializer = KeywordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KeywordDetail(APIView):
    def get(self, request, keyword_id, format=None):
        """
        Get keyword detail
        """
        keyword = get_object_or_404(Keyword, pk=keyword_id)
        serializer = KeywordSerializer(keyword)
        return Response(serializer.data)

    def put(self, request, keyword_id, format=None):
        """
        Edit keyword
        ---
        serializer: administrator.serializers.KeywordSerializer
        """
        keyword = get_object_or_404(Keyword, pk=keyword_id)
        serializer = KeywordSerializer(keyword, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, keyword_id, format=None):
        """
        Delete keyword (inactive keyword, you should edit is_active attribute to revert this change)
        ---
        serializer: administrator.serializers.KeywordSerializer
        """
        keyword = get_object_or_404(Keyword, pk=keyword_id)
        keyword.is_active = False
        keyword.save()
        serializer = KeywordSerializer(keyword)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class SubcategoryList(APIView):
    def get(self, request, format=None):
        """
        List all subcategories
        """
        subcategories = get_list_or_404(Subcategory)
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create new subcategory
        ---
        serializer: administrator.serializers.SubcategorySerializer
        """
        serializer = SubcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubcategoryDetail(APIView):
    def get(self, request, subcategory_id, format=None):
        """
        Get subcategory detail
        """
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        serializer = SubcategorySimpleSerializer(subcategory)
        return Response(serializer.data)

    def put(self, request, subcategory_id, format=None):
        """
        Edit subcategory
        ---
        serializer: administrator.serializers.SubcategorySerializer
        """
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        serializer = SubcategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, subcategory_id, format=None):
        """
        Edit categories relationship to subcategories
        ---
        parameters:
        - name: body
          required: true
          paramType: body
          pytype: administrator.serializers.CategoryPKListSerializer
        """
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        serializer = CategoryPKListSerializer(data=request.data)
        if serializer.is_valid():
            category_list = request.data['categories']
            subcategory.category = category_list
            response_serializer = SubcategorySimpleSerializer(subcategory)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subcategory_id, format=None):
        """
        Delete subcategory (inactive subcategory, you should edit is_active attribute to revert this change)
        ---
        serializer: administrator.serializers.SubcategorySerializer
        """
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        subcategory.is_active = False
        subcategory.save()
        serializer = SubcategorySerializer(subcategory)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
