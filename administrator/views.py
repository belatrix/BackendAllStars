from categories.models import Category, Keyword, Subcategory
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CategorySimpleSerializer, CategorySerializer, CategoryPKListSerializer
from .serializers import KeywordSerializer, SubcategorySerializer, SubcategorySimpleSerializer
from .serializers import SubcategoryPKListSerializer
from .pagination import AdministratorPagination


class CategoryList(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        """
        List all categories
        """
        categories = get_list_or_404(Category)
        paginator = AdministratorPagination()
        results = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

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
    permission_classes = (IsAdminUser,)

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
    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        """
        List all keywords (tags, skills) or result list if you use ?search=term%of%search
        ---
        parameters:
        - name: search
          required: false
          type: string
          paramType: query
        """
        if request.GET.get('search'):
            request_terms = request.GET.get('search')
            search_terms_array = request_terms.split()

            initial_term = search_terms_array[0]
            keywords = Keyword.objects.filter(Q(name__icontains=initial_term))

            if len(search_terms_array) > 1:
                for term in range(1, len(search_terms_array)):
                    keywords = keywords.filter(Q(name__icontains=search_terms_array[term]))
        else:
            keywords = get_list_or_404(Keyword)
        paginator = AdministratorPagination()
        results = paginator.paginate_queryset(keywords, request)
        serializer = KeywordSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

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
    permission_classes = (IsAdminUser,)

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
    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        """
        List all subcategories
        """
        subcategories = get_list_or_404(Subcategory)
        paginator = AdministratorPagination()
        results = paginator.paginate_queryset(subcategories, request)
        serializer = SubcategorySerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

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
    permission_classes = (IsAdminUser,)

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


class DeleteCategories(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request, id, kind, format=None):
        """
        WARNING: Force delete
        """
        if kind == 'category':
            kind = get_object_or_404(Category, pk=id)
        elif kind == 'subcategory':
            kind = get_object_or_404(Subcategory, pk=id)
        elif kind == 'keyword':
            kind = get_object_or_404(Keyword, pk=id)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        kind.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
