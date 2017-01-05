from .serializers import StarSerializer, StarBulkSerializer
from .serializers import StarTopEmployeeLists, StarEmployeeCategoriesSerializer, StarEmployeeKeywordsSerializer
from .serializers import StarKeywordList, StarInputSerializer, StarSmallSerializer
from .serializers import EmployeeBadgeListSerializer, EmployeeBadgeSerializer, EmployeeGroupedListSerializer
from .models import Badge, EmployeeBadge, Star
from constance import config
from activities.models import Activity
from employees.models import Employee
from categories.models import Category, Keyword
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from utils.send_messages import send_push_notification


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def give_star_to(request, from_employee_id, to_employee_id):
    """
    This endpoint saves stars on both employees (from and to).
    ---
    response_serializer: stars.serializers.StarInputSerializer
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
        keyword = get_object_or_404(Keyword, pk=request.data['keyword'])

        if from_user.is_blocked:
            content = {'detail': config.USER_BLOCKED_TO_GIVE_STARS}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif to_user.is_blocked:
            content = {'detail': config.USER_BLOCKED_TO_RECEIVED_STARS}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Create data object to save
        data = {"category": category.id,
                "keyword": keyword.id,
                "text": text,
                "from_user": from_user.id,
                "to_user": to_user.id}

        # Validate serializer with data provided.
        serializer = StarInputSerializer(data=data)
        if serializer.is_valid():
            # Save recommendation
            serializer.save()

            # Add 1 to employee given points
            from_user.add_stars_given(1)
            from_user.save()

            current_level = to_user.level

            # Add points to to_user according category weight
            if from_user.position:
                weight = from_user.position.weight
            else:
                weight = 1
            to_user.add_stars(weight)
            message = config.RECOMMENDATION_MESSAGE % (weight, from_user.first_name, from_user.last_name)
            send_push_notification(to_user, message)
            to_user.evaluate_level()
            to_user.save()

            # Add activity log if user level up
            if to_user.level != current_level:
                message = config.LEVEL_UP_TEXT % (to_user.first_name, to_user.last_name, to_user.level)
                activity = Activity.objects.create(text=message, to_user=to_user)
                send_push_notification(to_user, message)
                activity.save()

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
            keyword = get_object_or_404(Keyword, pk=request.data['keyword'])

            # Create data object to save
            data = {"category": category.id,
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

                    current_level = to_user.level

                    # Add points to to_user according category weight
                    if from_user.position:
                        weight = from_user.position.weight
                    else:
                        weight = 1

                    to_user.add_stars(weight)
                    message = config.RECOMMENDATION_MESSAGE % (weight, from_user.first_name, from_user.last_name)
                    send_push_notification(to_user, message)
                    to_user.evaluate_level()
                    to_user.save()

                    # Add activity log if user level up
                    if to_user.level != current_level:
                        message = config.LEVEL_UP_TEXT % (to_user.first_name, to_user.last_name, to_user.level)
                        activity = Activity.objects.create(text=message, to_user=to_user)
                        activity.save()

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
def stars_employee_list_group_by_category(request, employee_id):
    """
    Returns stars list from employee grouped by categories
    ---
    serializer: stars.serializers.StarEmployeeCategoriesSerializer
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
        employee_stars = Star.objects.filter(to_user=employee).values('category__pk',
                                                                      'category__name').annotate(num_stars=Count('category')).order_by('-num_stars',
                                                                                                                                       'category__name')
        paginator = PageNumberPagination()
        result = paginator.paginate_queryset(employee_stars, request)
        serializer = StarEmployeeCategoriesSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def stars_employee_list_group_by_keyword(request, employee_id):
    """
    Returns stars list from employee grouped by categories
    ---
    serializer: stars.serializers.StarEmployeeKeywordsSerializer
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
        employee_stars = Star.objects.filter(to_user=employee).values('keyword__pk',
                                                                      'keyword__name').annotate(num_stars=Count('keyword')).order_by('-num_stars',
                                                                                                                                     'keyword__name')
        paginator = PageNumberPagination()
        result = paginator.paginate_queryset(employee_stars, request)
        serializer = StarEmployeeKeywordsSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def stars_employee_list_group_by_category_detail(request, employee_id, category_id):
    """
    Returns stars list detail from employee divided by category
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
        category = get_object_or_404(Category, pk=category_id)
        stars = Star.objects.filter(to_user=employee, category=category).order_by('-date')
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(stars, request)
        serializer = StarSmallSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def stars_employee_list_group_by_keyword_detail(request, employee_id, keyword_id):
    """
    Returns stars list detail from employee divided by keyword
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
        keyword = get_object_or_404(Keyword, pk=keyword_id)
        stars = Star.objects.filter(to_user=employee, keyword=keyword).order_by('-date')
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(stars, request)
        serializer = StarSmallSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def stars_top_employee_lists(request, top_number, kind, id):
    """
    Returns stars top {top_number} list according to {kind} (category, keyword) {id} (kind_id)
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
                top_list = Star.objects.filter(category__id=id).values(
                    'to_user__pk',
                    'to_user__username',
                    'to_user__first_name',
                    'to_user__last_name',
                    'to_user__level'
                    'to_user__avatar').annotate(num_stars=Count('to_user')).order_by('-num_stars')[:top_number]
            elif kind == 'keyword':
                top_list = Star.objects.filter(keyword__id=id).values(
                    'to_user__pk',
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
    parameters:
    - name: search
      required: false
      type: string
      paramType: query
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


@api_view(['POST', ])
@permission_classes((IsAuthenticated, IsAdminUser))
def give_badge_to(request, badge_id, to_employee_id, from_employee_id):
    """
    This endpoint saves badge assignation to employee
    ---
    response_serializer: stars.serializers.EmployeeBadgeSerializer
    responseMessages:
    - code: 400
      message: Bad request
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found (from_employee_id or to_employee_id or badge_id)
    - code: 406
      message: User is unable to give stars to itself.
    """
    if to_employee_id == from_employee_id:
        content = {'detail': config.USER_UNABLE_TO_GIVE_BADGES_ITSELF}
        return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
    elif request.method == 'POST':
        badge = get_object_or_404(Badge, pk=badge_id)
        to_employee = get_object_or_404(Employee, pk=to_employee_id)
        from_employee = get_object_or_404(Employee, pk=from_employee_id)
        try:
            employee_badge = EmployeeBadge.objects.create(to_user=to_employee, assigned_by=from_employee, badge=badge)
        except Exception as e:
            print(e)
            content = {'detail': config.BADGE_UNIQUE_CONSTRAINT_FAILED}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = EmployeeBadgeSerializer(employee_badge)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def badges_employee_list(request, employee_id):
    """
    Returns badge list from employee
    ---
    response_serializer: stars.serializers.EmployeeBadgeSerializer
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
        employee_bages = EmployeeBadge.objects.filter(to_user=employee)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(employee_bages, request)
        serializer = EmployeeBadgeSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def employee_list_group_by_badges(request):
    """
    Returns badge list with employee counter or result list if you use ?search=
    ---
    response_serializer: stars.serializers.EmployeeBadgeListSerializer
    parameters:
    - name: search
      required: false
      type: string
      paramType: query
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
            badge_list = EmployeeBadge.objects.filter(
                Q(badge__name__icontains=search_term)).values('badge__pk',
                                                              'badge__name').annotate(num_employees=Count('to_user')).order_by('-num_employees')
        else:
            badge_list = EmployeeBadge.objects.all().values('badge__pk', 'badge__name').annotate(num_employees=Count('to_user')).order_by('-num_employees')
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(badge_list, request)
        serializer = EmployeeBadgeListSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def employee_list_group_by_badges_detail(request, badge_id):
    """
    Returns employee list grouped by badge, you should provide badge_id
    ---
    response_serializer: stars.serializers.EmployeeGroupedListSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        badge = get_object_or_404(Badge, pk=badge_id)
        employee_list = EmployeeBadge.objects.filter(badge=badge).values(
            'to_user__pk',
            'to_user__username',
            'to_user__first_name',
            'to_user__last_name',
            'to_user__level',
            'to_user__avatar')
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(employee_list, request)
        serializer = EmployeeGroupedListSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
