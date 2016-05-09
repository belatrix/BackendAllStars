from .models import Employee, Location, Role
from .serializers import EmployeeSerializer, EmployeeAvatarSerializer, EmployeeListSerializer
from .serializers import EmployeeLocationListSerializer, EmployeeRoleListSerializer
from .serializers import EmployeeTopTotalScoreList, EmployeeTopLevelList
from .serializers import EmployeeTopCurrentMonthList, EmployeeTopLastMonthList
from .serializers import EmployeeTopCurrentYearList, EmployeeTopLastYearList
from categories.serializers import CategorySerializer
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
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
from uuid import uuid4


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
    - name: email
      required: true
      paramType: string
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
            except Exception as e:
                print e
                content = {'detail': 'User already exists, maybe you need a password reset.'}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

            try:
                send_email = EmailMessage(subject, message, to=[email])
                send_email.send()
            except Exception as e:
                print e
                content = {'detail': 'User was created, but there are problems with email service, please contact an administrator.'}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

            content = {'detail': 'Successful user creation'}
            return Response(content, status=status.HTTP_201_CREATED)
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
def employee_deactivated_list(request):
    """
    Returns the full employee deactivated list
    ---
    serializer: employees.serializers.EmployeeListSerializer
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee_list = get_list_or_404(Employee, is_active=False)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(employee_list, request)
        serializer = EmployeeListSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def employee_list(request):
    """
    Returns the full employee list or result list if you use ?search=
    ---
    serializer: employees.serializers.EmployeeListSerializer
    parameters:
    - name: search
      required: false
      type: string
      paramType: query
    responseMessages:
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        if request.GET.get('search'):
            search_term = request.GET.get('search')
            employee_list = Employee.objects.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(username__icontains=search_term)).filter(is_active=True)
        else:
            employee_list = get_list_or_404(Employee, is_active=True)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(employee_list, request)
        serializer = EmployeeListSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


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
def employee_reset_password(request, employee_email):
    if request.method == 'GET':
        employee = get_object_or_404(Employee, email=employee_email)

        # Generate random uuid and save in employee
        uuid_code = uuid4()
        employee.reset_password_code = str(uuid_code)
        employee.save()

        # Send email with reset password confirmation url
        subject = settings.EMPLOYEE_RESET_PASSWORD_CONFIRMATION_SUBJECT
        current_site = Site.objects.get_current()
        employee_reset_password_api = reverse('employees:employee_reset_password', args=[employee.email])
        url = current_site.domain + employee_reset_password_api + employee.reset_password_code
        message = 'If you want to reset your password please confirm the request, clicking here: %s' % (url)

        try:
            send_email = EmailMessage(subject, message, to=[employee.email])
            send_email.send()
        except Exception as e:
            print e
            content = {'detail': 'There are problems with email service, please contact an administrator.'}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        content = {'detail': 'Confirmation email sent.',
                   'email': employee.email,
                   'reset_password_code': employee.reset_password_code}
        return Response(content, status=status.HTTP_200_OK)


@api_view(['GET', ])
def employee_reset_password_confirmation(request, employee_email, employee_uuid):
    if request.method == 'GET':
        employee = get_object_or_404(Employee, email=employee_email, reset_password_code=employee_uuid)
        random_password = Employee.objects.make_random_password()
        employee.set_password(random_password)
        employee.reset_password_code = None
        employee.save()

        # Send confirmation email
        subject = settings.EMPLOYEE_RESET_PASSWORD_SUCCESSFUL_SUBJECT
        message = 'Your new password is: %s' % (random_password)
        try:
            send_email = EmailMessage(subject, message, to=[email])
            send_email.send()
        except Exception as e:
            print e
            content = {'detail': 'Password was reset, but there are problems with email service, please contact an administrator.'}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        content = {'detail': 'Successful password creation, email has been sent'}
        return Response(content, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
def employee_update(request, employee_id):
    """
    This endpoint update skype, first_name, last_name and location
    ---
    response_serializer: employees.serializers.EmployeeSerializer
    parameters:
    - name: first_name
      required: true
      paramType: string
    - name: last_name
      required: true
      paramType: string
    - name: skype_id
      required: true
      paramType: string
    - name: location
      description: location id
      paramType: string
    """
    if request.method == 'PATCH':
        try:
            employee = get_object_or_404(Employee, pk=employee_id)
            employee.skype_id = request.data['skype_id']
            employee.first_name = request.data['first_name']
            employee.last_name = request.data['last_name']
            employee.location = get_object_or_404(Location, pk=request.data['location'])
            employee.save()
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            raise APIException(e)


@api_view(['POST', ])
def employee_update_password(request, employee_id):
    """
    This endpoint update employee password
    ---
    response_serializer: employees.serializers.EmployeeSerializer
    parameters:
    - name: current_password
      required: true
      paramType: string
    - name: new_password
      required: true
      paramType: string
    """
    if request.method == 'POST':
        try:
            current_password = request.data['current_password']
            new_password = request.data['new_password']
        except Exception as e:
            raise APIException(e)
        employee = get_object_or_404(Employee, pk=employee_id)
        if current_password == new_password:
            content = {'detail': 'new and current password are equal.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif employee.check_password(current_password):
            employee.set_password(new_password)
            employee.save()
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            content = {'detail': 'Current password is wrong.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def top(request, kind, quantity):
    """
    Returns top {quantity} list, {kind} (total_score, level, last_month_score, current_month_score, last_year_score, current_year_score)
    ---
    serializer: employees.serializers.EmployeeTopListSerializer
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
            if kind == 'total_score':
                serializer = EmployeeTopTotalScoreList(employee_list, many=True)
            elif kind == 'level':
                serializer = EmployeeTopLevelList(employee_list, many=True)
            elif kind == 'current_month_score':
                serializer = EmployeeTopCurrentMonthList(employee_list, many=True)
            elif kind == 'current_year_score':
                serializer = EmployeeTopCurrentYearList(employee_list, many=True)
            elif kind == 'last_month_score':
                serializer = EmployeeTopLastMonthList(employee_list, many=True)
            elif kind == 'last_year_score':
                serializer = EmployeeTopLastYearList(employee_list, many=True)
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
        - name: username
          required: true
          paramType: string
        - name: password
          required: true
          :paramType: string
        """
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})
