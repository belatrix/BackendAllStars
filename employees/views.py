from .models import Employee, Location, Role
from .serializers import EmployeeSerializer, EmployeeAvatarSerializer, EmployeeListSerializer
from .serializers import EmployeeLocationListSerializer, EmployeeRoleListSerializer
from .serializers import EmployeeTopTotalScoreList, EmployeeTopLevelList
from .serializers import EmployeeTopCurrentMonthList, EmployeeTopLastMonthList
from .serializers import EmployeeTopCurrentYearList, EmployeeTopLastYearList
from categories.serializers import CategorySerializer
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', ])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def employee_list(request):
    """
    Returns the full employee list
    ---
    serializer: employees.serializers.EmployeeListSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee_list = get_list_or_404(Employee, is_active=True)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(employee_list, request)
        serializer = EmployeeListSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
def employee(request, employee_id):
    """
    Returns employee details
    ---
    serializer: employees.serializers.EmployeeSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
def employee_activate(request, employee_id):
    """
    Activate employee account
    ---
    response_serializer: employees.serializers.EmployeeSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'PATCH':
        employee = get_object_or_404(Employee, pk=employee_id)
        employee.is_active = True
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
def employee_creation(request):
    """
    This endpoint creates a new user with provided email @belatrixsf.com
    ---
    parameters:
    - name: body
      description: JSON Object containing email address at belatrixsf.com
      required: true
      paramType: body
      pytype: employees.serializers.EmployeeCreationSerializer
    """
    if request.method == 'POST':
        email = request.data['email']
        username = email.split('@')[0]
        domain = email.split('@')[1]
        if domain == settings.EMAIL_DOMAIN:
            random_password = Employee.objects.make_random_password()
            subject = settings.EMPLOYEE_CREATION_SUBJECT
            message = 'Your initial random password is %s' % (random_password)
            try:
                Employee.objects.create_user(username, password=random_password, email=email)
                send_email = EmailMessage(subject, message, to=[email])
                send_email.send()
                content = {'detail': 'Successful user creation'}
                return Response(content, status=status.HTTP_201_CREATED)
            except Exception as e:
                content = 'User already exists or is not available to create a new one with this email address.'
                raise APIException(content)
        else:
            content = {'detail': 'User creation is not available for other email domains.'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH', ])
def employee_deactivate(request, employee_id):
    """
    Deactivate employee account
    ---
    response_serializer: employees.serializers.EmployeeSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'PATCH':
        employee = get_object_or_404(Employee, pk=employee_id)
        employee.is_active = False
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
def employee_location_list(request):
    """
    Returns employee location full list
    ---
    serializer: employees.serializers.EmployeeLocationListSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        location_list = get_list_or_404(Location)
        serializer = EmployeeLocationListSerializer(location_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def employee_role_list(request):
    """
    Returns employee role full list
    ---
    serializer: employees.serializers.EmployeeRoleListSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        role_list = get_list_or_404(Role)
        serializer = EmployeeRoleListSerializer(role_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def employee_avatar(request, employee_id):
    """
    Returns employee avatar
    ---
    serializer: employees.serializers.EmployeeAvatarSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        serializer = EmployeeAvatarSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def employee_categories(request, employee_id):
    """
    Returns employee category list
    ---
    serializer: categories.serializers.CategorySerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        serializer = CategorySerializer(employee.categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def top(request, kind, quantity):
    """
    Returns top {quantity} list, {kind} (total_score, level, last_month_score, current_month_score, last_year_score, current_year_score)
    ---
    serializer: employees.serializers.EmployeeListSerializer
    responseMessages:
    - code: 404
      message: Not found
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 500
      message: Internal server error, cannot resolve keyword into field.
    """
    try:
        if request.method == 'GET':
            employee_list = Employee.objects.filter(is_active=True).order_by('-' + kind)[:quantity]
            if kind == 'total_score': serializer = EmployeeTopTotalScoreList(employee_list, many=True)
            elif kind == 'level': serializer = EmployeeTopLevelList(employee_list, many=True)
            elif kind == 'current_month_score': serializer=EmployeeTopCurrentMonthList(employee_list, many=True)
            elif kind == 'current_year_score': serializer=EmployeeTopCurrentYearList(employee_list, many=True)
            elif kind == 'last_month_score': serializer=EmployeeTopLastMonthList(employee_list, many=True)
            elif kind == 'last_year_score': serializer=EmployeeTopLastYearList(employee_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        raise APIException(e)


@api_view(['GET', ])
def search(request, search_term):
    """
    Returns employee list according search term
    ---
    serializer: employees.serializers.EmployeeListSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee_list = Employee.objects.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(username__icontains=search_term)).filter(is_active=True)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(employee_list, request)
        serializer = EmployeeListSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Returns a token and user_id, for credentials provided.
        ---
        response_serializer: employees.serializers.EmployeeAuthenticationResponse
        responseMessages:
        - code: 400
          message: Bad request
        parameters:
        - name: body
          description: JSON Object containing two parameters = username and password.
          required: true
          paramType: body
          pytype: rest_framework.authtoken.serializers.AuthTokenSerializer
        """
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})
