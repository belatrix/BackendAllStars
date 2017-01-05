from categories.models import Category, Keyword
from employees.models import Position
from stars.models import Badge
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CategorySerializer, KeywordSerializer, BadgeSerializer, PositionSerializer
from .pagination import AdministratorPagination


class BadgeList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, format=None):
        """
        List all badges
        """
        badges = get_list_or_404(Badge)
        paginator = AdministratorPagination()
        results = paginator.paginate_queryset(badges, request)
        serializer = BadgeSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        Create new badge
        ---
        serializer: administrator.serializers.BadgeSerializer
        """
        serializer = BadgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BagdeDetail(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, badge_id, format=None):
        """
        Get badge details
        """
        badge = get_object_or_404(Badge, pk=badge_id)
        serializer = BadgeSerializer(badge)
        return Response(serializer.data)

    def put(self, request, badge_id, format=None):
        """
        Edit badge
        ---
        serializer: administrator.serializers.BadgeSerializer
        """
        badge = get_object_or_404(Badge, pk=badge_id)
        serializer = BadgeSerializer(badge, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, badge_id, format=None):
        """
        Delete badge (inactive badge, you should edit is_active attribute to revert this change)
        ---
        serializer: administrator.serializers.BadgeSerializer
        """
        badge = get_object_or_404(Badge, pk=badge_id)
        badge.is_active = False
        badge.save()
        serializer = BadgeSerializer(badge)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class CategoryList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

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
        serializer: administrator.serializers.CategorySerializer
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

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
        serializer: administrator.serializers.CategorySerializer
        """
        category = get_object_or_404(Category, pk=category_id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class KeywordList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

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
    permission_classes = (IsAdminUser, IsAuthenticated)

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


class PositionList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, format=None):
        """
        List all employee positions
        """
        positions = get_list_or_404(Position)
        paginator = AdministratorPagination()
        results = paginator.paginate_queryset(positions, request)
        serializer = PositionSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        Create new position
        ---
        serializer: administrator.serializers.PositionSerializer
        """
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PositionDetail(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, position_id, format=None):
        """
        Get position detail
        """
        position = get_object_or_404(Position, pk=position_id)
        serializer = PositionSerializer(position)
        return Response(serializer.data)\

    def put(self, request, position_id, format=None):
        """
        Edit position
        ---
        serializer: administrator.serializers.PositionSerializer
        """
        position = get_object_or_404(Position, pk=position_id)
        serializer = PositionSerializer(position, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, position_id, format=None):
        """
        Deactivate position, you should edit is_active attribute to revert this change
        ---
        serializer: administrator.serializers.PositionSerializer
        """
        position = get_object_or_404(Position, pk=position_id)
        position.is_active = False
        position.save()
        serializer = PositionSerializer(position)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class ObjectsDelete(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def delete(self, request, id, kind, format=None):
        """
        WARNING: Force delete
        """
        if kind == 'badge':
            kind = get_object_or_404(Badge, pk=id)
        elif kind == 'category':
            kind = get_object_or_404(Category, pk=id)
        elif kind == 'keyword':
            kind = get_object_or_404(Keyword, pk=id)
        elif kind == 'position':
            kind = get_object_or_404(Position, pk=id)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        kind.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
