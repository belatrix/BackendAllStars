from .serializers import StarSerializer, StarSmallSerializer, StarEmployeesSubcategoriesSerializer, StarTopEmployeeLists
from .models import Star
from employees.models import Employee
from categories.models import Category, Subcategory
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform csrf check


@api_view(['POST', ])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def give_star_to(request, from_employee_id, to_employee_id):
    """
    This endpoint saves stars on both employees (from and to).
    ---
    response_serializer: StarSerializer
    responseMessages:
    - code: 400
      message: Bad request
    - code: 404
      message: Not found (from_employee_id or to_employee_id or category or subcategory)
    parameters:
    - name: body
      description: JSON Object containing two or three parameters = category(id), subcategory(id)  and text(optional).
      required: true
      paramType: body
      pytype: stars.serializers.StarSwaggerSerializer
    """
    # Set None as initial values for variables in content json
    category_id = None
    subcategory_id = None
    text = None

    if request.method == 'POST':
        # Set values from request.data from POST
        text = (request.data['text'] if 'text' in request.data.keys() else None)
        from_user = get_object_or_404(Employee, pk=from_employee_id)
        to_user = get_object_or_404(Employee, pk=to_employee_id)
        category_id = (request.data['category'] if request.data['category'] else None)
        category = get_object_or_404(Category, pk=category_id)
        subcategory_id = (request.data['subcategory'] if request.data['subcategory'] else None)
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)

        # Create data object to save
        data = {"category": category.id,
                "subcategory": subcategory.id,
                "text": text,
                "from_user": from_user.id,
                "to_user": to_user.id}

        # Validate serializer with data provided.
        serializer = StarSerializer(data=data)
        if serializer.is_valid():
            # Save recommendation
            serializer.save()

            # Add 1 point to from_user
            from_user.score += 1
            from_user.current_month_score += 1
            from_user.evaluate_level()
            from_user.save()

            # Add points to to_user according category weight
            to_user.score += category.weight
            to_user.current_month_score += category.weight
            to_user.evaluate_level()
            to_user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def star(request, star_id):
    """
    Returns star detail
    ---
    serializer: stars.serializers.StarSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        star = get_object_or_404(Star, pk=star_id)
        serializer = StarSerializer(star)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def stars_employee_list(request, employee_id):
    """
    Returns stars list from employee
    ---
    serializer: stars.serializers.StarSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        employee_stars = Star.objects.filter(to_user=employee)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(employee_stars, request)
        serializer = StarSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
def stars_employee_subcategory_list(request, employee_id):
    """
    Returns stars list from employee grouped by subcategories
    ---
    serializer: stars.serializers.StarEmployeesSubcategoriesSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        employee_stars = Star.objects.filter(to_user=employee).values('subcategory__pk', 'subcategory__name').annotate(num_stars=Count('subcategory')).order_by('-num_stars')
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(employee_stars, request)
        serializer = StarEmployeesSubcategoriesSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
def stars_employee_subcategory_detail_list(request, employee_id, subcategory_id):
    """
    Returns stars list detail from employee divided by subcategory
    ---
    serializer: stars.serializers.StarSmallSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        stars = Star.objects.filter(to_user=employee, subcategory=subcategory)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(stars, request)
        serializer = StarSmallSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
def stars_top_employee_lists(request, top_number, kind, id):
    """
    Returns stars top {top_number} list according to {kind} (category, subcategory) {id} (kind_id)
    ---
    serializer: stars.serializers.StarTopEmployeeLists
    responseMessages:
    - code: 404
      message: Not found
    - code: 412
      message: Precondition failed, kind should be category or subcategory
    """
    try:
        if request.method == 'GET':
            if kind == 'category':
                top_list = Star.objects.filter(category__id=id).values('to_user__id', 'to_user__username', 'to_user__first_name', 'to_user__last_name').annotate(num_stars=Count('to_user')).order_by('-num_stars')[:top_number]
            elif kind == 'subcategory':
                top_list = Star.objects.filter(subcategory__id=id).values('to_user__id', 'to_user__username', 'to_user__first_name', 'to_user__last_name').annotate(num_stars=Count('to_user')).order_by('-num_stars')[:top_number]
            else:
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)
            serializer = StarTopEmployeeLists(top_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        raise APIException(e)
