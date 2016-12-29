from categories.models import Category, Keyword
from employees.models import Employee
from employees.serializers import EmployeeSerializer, EmployeeSetListSerializer
from constance import config
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CategorySerializer
from .serializers import KeywordSerializer
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
        serializer: administrator.serializers.CategorySerializer
        """
        serializer = CategorySerializer(data=request.data)
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


class CategoriesModelsDelete(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request, id, kind, format=None):
        """
        WARNING: Force delete
        """
        if kind == 'category':
            kind = get_object_or_404(Category, pk=id)
        elif kind == 'keyword':
            kind = get_object_or_404(Keyword, pk=id)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        kind.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH', ])
@permission_classes((IsAdminUser, IsAuthenticated))
def employee_admin(request, employee_id, action):
    """
    Set or unset admin permission to employee, action could be true or false
    ---
    response_serializer: employees.serializers.EmployeeSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'PATCH':
        employee = get_object_or_404(Employee, pk=employee_id)
        if action == 'true':
            employee.is_staff = True
        elif action == 'false':
            employee.is_staff = False
        else:
            pass
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['PATCH', ])
@permission_classes((IsAdminUser, IsAuthenticated))
def employee_set_list(request, employee_id):
    """
    Endpoint to set list of positions to employee, type can be position or role
    ---
    parameters:
    - name: body
      required: true
      paramType: body
      pytype: employees.serializers.EmployeeSetListSerializer
    responseMessages:
    - code: 400
      message: Bad request
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 406
      message: Request not acceptable
    """
    if request.method == 'PATCH':
        employee = get_object_or_404(Employee, pk=employee_id)
        serializer = EmployeeSetListSerializer(data=request.data)
        errors = []
        if serializer.is_valid():
            list_type = request.data['type']
            elements_list = request.data['set_id_list']
            if list_type == 'position':
                employee.position = elements_list
                employee.save()
            elif list_type == 'role':
                employee.role = elements_list
                employee.save()
            else:
                errors.append(config.SET_LIST_TYPE_UNKNOWN)
        else:
            errors.append(serializer.errors)

        if len(errors) == 0:
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            content = {'detail': errors}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
