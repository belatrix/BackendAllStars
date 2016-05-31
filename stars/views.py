from .serializers import StarSerializer, StarSmallSerializer, StarBulkSerializer
from .serializers import StarEmployeesSubcategoriesSerializer, StarTopEmployeeLists
from .serializers import StarKeywordList
from .models import Star
from constance import config
from employees.models import Employee
from categories.models import Category, Keyword, Subcategory
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def give_star_to(request, from_employee_id, to_employee_id):
    """
    This endpoint saves stars on both employees (from and to).
    This endpoint saves stars on both employees (from and to).
    ---
    response_serializer: stars.serializers.StarSerializer
    responseMessages:
    - code: 400
      message: Bad request
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found (from_employee_id or to_employee_id or category or subcategory)
    - code: 406
      message: User is unable to give stars to itself.
    parameters:
    - name: category
      description: category id
      required: true
      paramType: string
    - name: subcategory
      description: subcategory id
      required: true
      paramType: string
    - name: keyword
      description: keyword id
      required: true
      paramType: string
    """
    if from_employee_id == to_employee_id:
        content = {'detail': config.USER_UNABLE_TO_GIVE_STARS_ITSELF}
        return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
    elif request.method == 'POST':
        # Set values from request.data from POST
        text = (request.data['text'] if 'text' in request.data.keys() else None)
        from_user = get_object_or_404(Employee, pk=from_employee_id)
        to_user = get_object_or_404(Employee, pk=to_employee_id)
        category = get_object_or_404(Category, pk=request.data['category'])
        subcategory = get_object_or_404(Subcategory, pk=request.data['subcategory'])
        keyword = get_object_or_404(Keyword, pk=request.data['keyword'])

        if from_user.is_blocked:
            content = {'detail': config.USER_BLOCKED_TO_GIVE_STARS}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif to_user.is_blocked:
            content = {'detail': config.USER_BLOCKED_TO_RECEIVED_STARS}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Create data object to save
        data = {"category": category.id,
                "subcategory": subcategory.id,
                "keyword": keyword.id,
                "text": text,
                "from_user": from_user.id,
                "to_user": to_user.id}

        # Validate serializer with data provided.
        serializer = StarSerializer(data=data)
        if serializer.is_valid():
            # Save recommendation
            serializer.save()

            # Add 1 to employee given points
            from_user.add_stars_given(1)
            from_user.save()

            # Add points to to_user according category weight
            to_user.add_stars(category.weight)
            to_user.evaluate_level()
            to_user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def give_star_to_many(request, from_employee_id):
    """
    This endpoint saves stars on many employees.
    ---
    response_serializer: stars.serializers.StarSerializer
    responseMessages:
    - code: 400
      message: Bad request
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found (from_employee_id or to_users or category or subcategory)
    - code: 406
      message: User is unable to give stars to itself.
    parameters:
    - name: body
      required: true
      paramType: body
      pytype: stars.serializers.StarBulkSerializer
    """
    if request.method == 'POST':
        serializer_bulk = StarBulkSerializer(data=request.data)
        errors = []
        stars_added = 0
        if serializer_bulk.is_valid():
            text = (request.data['text'] if 'text' in request.data.keys() else None)
            from_user = get_object_or_404(Employee, pk=from_employee_id)
            category = get_object_or_404(Category, pk=request.data['category'])
            subcategory = get_object_or_404(Subcategory, pk=request.data['subcategory'])
            keyword = get_object_or_404(Keyword, pk=request.data['keyword'])

            # Create data object to save
            data = {"category": category.id,
                    "subcategory": subcategory.id,
                    "keyword": keyword.id,
                    "text": text,
                    "from_user": from_user.id}

            for user_pk in request.data['to_users']:
                data.update({"to_user": int(user_pk)})
                serializer = StarSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    stars_added += 1

                    # Add points
                    to_user = get_object_or_404(Employee, pk=user_pk)
                    from_user.add_stars_given(1)
                    from_user.save()
                    to_user.add_stars(category.weight)
                    to_user.evaluate_level()
                    to_user.save()
                else:
                    errors.append(serializer.errors)
        else:
            errors.append(serializer_bulk.errors)

        if len(errors) == 0:
            content = {'detail': config.SUCCESSFULLY_STARS_ADDED}
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            stars_results = {"stars_added": stars_added}
            detail = {'detail': errors}
            content = stars_results.copy()
            content.update(detail)
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def star(request, star_id):
    """
    Returns star detail
    ---
    serializer: stars.serializers.StarSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        star = get_object_or_404(Star, pk=star_id)
        serializer = StarSerializer(star)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def stars_employee_list(request, employee_id):
    """
    Returns stars list from employee
    ---
    serializer: stars.serializers.StarSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
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
@permission_classes((IsAuthenticated,))
def stars_employee_subcategory_list(request, employee_id):
    """
    Returns stars list from employee grouped by subcategories
    ---
    serializer: stars.serializers.StarEmployeesSubcategoriesSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        employee_stars = Star.objects.filter(to_user=employee).values('subcategory__pk', 'subcategory__name').annotate(num_stars=Count('subcategory')).order_by('-num_stars', 'subcategory__name')
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(employee_stars, request)
        serializer = StarEmployeesSubcategoriesSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def stars_employee_subcategory_detail_list(request, employee_id, subcategory_id):
    """
    Returns stars list detail from employee divided by subcategory
    ---
    serializer: stars.serializers.StarSmallSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        stars = Star.objects.filter(to_user=employee, subcategory=subcategory).order_by('-date')
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(stars, request)
        serializer = StarSmallSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def stars_top_employee_lists(request, top_number, kind, id):
    """
    Returns stars top {top_number} list according to {kind} (category, subcategory, keyword) {id} (kind_id)
    ---
    serializer: stars.serializers.StarTopEmployeeLists
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found
    - code: 412
      message: Precondition failed, kind should be category or subcategory
    """
    try:
        if request.method == 'GET':
            if kind == 'category':
                top_list = Star.objects.filter(category__id=id).values('to_user__pk',
                                                                       'to_user__username',
                                                                       'to_user__first_name',
                                                                       'to_user__last_name',
                                                                       'to_user__level'
                                                                       'to_user__avatar').annotate(num_stars=Count('to_user')).order_by('-num_stars')[:top_number]
            elif kind == 'subcategory':
                top_list = Star.objects.filter(subcategory__id=id).values('to_user__pk',
                                                                          'to_user__username',
                                                                          'to_user__first_name',
                                                                          'to_user__last_name',
                                                                          'to_user__level',
                                                                          'to_user__avatar').annotate(num_stars=Count('to_user')).order_by('-num_stars')[:top_number]
            elif kind == 'keyword':
                top_list = Star.objects.filter(keyword__id=id).values('to_user__pk',
                                                                      'to_user__username',
                                                                      'to_user__first_name',
                                                                      'to_user__last_name',
                                                                      'to_user__level',
                                                                      'to_user__avatar').annotate(num_stars=Count('to_user')).order_by('-num_stars')[:top_number]
            else:
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)
            serializer = StarTopEmployeeLists(top_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        raise APIException(e)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def stars_keyword_list(request):
    """
    Returns stars list grouped by keyword or result list if you use ?search=
    ---
    serializer: stars.serializers.StarKeywordList
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        if request.GET.get('search'):
            search_term = request.GET.get('search')
            star_list = Star.objects.filter(
                Q(keyword__name__icontains=search_term)).values('keyword__pk',
                                                                'keyword__name').annotate(num_stars=Count('keyword')).order_by('-num_stars')
        else:
            star_list = Star.objects.all().values('keyword__pk', 'keyword__name').annotate(num_stars=Count('keyword')).order_by('-num_stars')
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(star_list, request)
        serializer = StarKeywordList(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def stars_keyword_list_detail(request, keyword_id):
    """
    Returns stars list detail for keyword id.
    ---
    response_serializer: stars.serializers.StarTopEmployeeLists
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        keyword = get_object_or_404(Keyword, pk=keyword_id)
        stars = Star.objects.filter(keyword=keyword).values(
            'to_user__pk',
            'to_user__username',
            'to_user__first_name',
            'to_user__last_name',
            'to_user__level',
            'to_user__avatar').annotate(num_stars=Count('keyword')).order_by('-num_stars')
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(stars, request)
        serializer = StarTopEmployeeLists(results, many=True)
        return paginator.get_paginated_response(serializer.data)
