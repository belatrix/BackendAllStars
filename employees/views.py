from .models import Employee, Location, Position, Role, EmployeeDevice
from .serializers import EmployeeSerializer, EmployeeAvatarSerializer, EmployeeListSerializer, EmployeeCreationListSerializer
from .serializers import EmployeeLocationListSerializer, EmployeePositionListSerializer, EmployeeRoleListSerializer
from .serializers import EmployeeTopTotalScoreList, EmployeeTopLevelList
from .serializers import EmployeeTopCurrentMonthList, EmployeeTopLastMonthList
from .serializers import EmployeeTopCurrentYearList, EmployeeTopLastYearList, EmployeeDeviceSerializer
from constance import config
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404
from re import match as regex_match
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import APIException, NotAcceptable
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def employee(request, employee_id):
    """
    Returns employee details
    ---
    serializer: employees.serializers.EmployeeSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated, IsAdminUser))
def employee_activate(request, employee_id, action):
    """
    Activate employee account, action could be true or false
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
            employee.is_active = True
        elif action == 'false':
            employee.is_active = False
        else:
            pass
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
@permission_classes((IsAdminUser, IsAuthenticated))
def employee_bulk_creation(request):
    """
    Endpoint to create users using email list
    ---
    parameters:
    - name: body
      required: true
      paramType: body
      pytype: employees.serializers.EmployeeCreationListSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 406
      message: Request not acceptable
    """
    if request.method == 'POST':
        serializer = EmployeeCreationListSerializer(data=request.data)
        errors = []
        users_created = 0
        if serializer.is_valid():
            email_list = request.data
            for email_object in email_list['emails']:
                email = email_object['email'].lower()
                if regex_match(r"[^@]+@[^@]+\.[^@]+", email):
                    username = email.split('@')[0].lower()
                    domain = email.split('@')[1].lower()
                    if domain in settings.EMAIL_DOMAIN_LIST:
                        if not Employee.objects.filter(email=email).exists():
                            new_employee = Employee.objects.create_user(username, password=request.data['password'], email=email)
                            new_employee.generate_reset_password_code()
                            new_employee.save()
                            users_created += 1
                        else:
                            errors.append(config.USER_EMAIL_ALREADY_REGISTERED % (email))
                    else:
                        errors.append(config.EMAIL_DOMAIN_FORBIDDEN % (domain))
                else:
                    errors.append(config.INVALID_EMAIL_ADDRESS % (email))
        else:
            errors.append(serializer.errors)

        if len(errors) == 0:
            content = {'detail': config.USER_SUCCESSFULLY_CREATED}
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            users_result = {"user_created": users_created}
            detail = {'detail': errors}
            content = users_result.copy()
            content.update(detail)
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated, IsAdminUser))
def employee_block(request, employee_id, action):
    """
    Block employee account, action could be true or false
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
            employee.is_blocked = True
        elif action == 'false':
            employee.is_blocked = False
        else:
            pass
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
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 406
      message: Request not acceptable
    """
    if request.method == 'POST':
        email = request.data['email'].lower()

        if regex_match(r"[^@]+@[^@]+\.[^@]+", email):
            username = email.split('@')[0].lower()
            domain = email.split('@')[1].lower()
        else:
            content = {'detail': config.INVALID_EMAIL_ADDRESS}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        if domain in settings.EMAIL_DOMAIN_LIST:
            random_password = Employee.objects.make_random_password(length=4, allowed_chars='beatrx23456789')
            subject = config.EMPLOYEE_CREATION_SUBJECT
            message = config.EMPLOYEE_CREATION_MESSAGE % (username, random_password)

            try:
                new_employee = Employee.objects.create_user(username, password=random_password, email=email)
                new_employee.generate_reset_password_code()
                new_employee.save()
            except Exception as e:
                print(e)
                content = {'detail': config.USER_EMAIL_ALREADY_REGISTERED % (email)}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

            try:
                send_email = EmailMessage(subject, message, to=[email])
                send_email.send()
            except Exception as e:
                print(e)
                content = {'detail': config.USER_SUCCESSFULLY_CREATED_EMAIL_ERROR}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

            content = {'detail': config.USER_SUCCESSFULLY_CREATED}
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            content = {'detail': config.EMAIL_DOMAIN_FORBIDDEN % (domain)}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def employee_deactivated_list(request, format=None):
    """
    Returns the full employee deactivated list
    ---
    serializer: employees.serializers.EmployeeListSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
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
@permission_classes((IsAuthenticated,))
def employee_list(request, format=None):
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
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        if request.GET.get('search'):
            request_terms = request.GET.get('search')
            search_terms_array = request_terms.split()

            initial_term = search_terms_array[0]
            employee_list = Employee.objects.filter(Q(first_name__icontains=initial_term) |
                                                    Q(last_name__icontains=initial_term) |
                                                    Q(username__icontains=initial_term)).filter(is_base_profile_complete=True)
            if len(search_terms_array) > 1:
                for term in range(1, len(search_terms_array)):
                    employee_list = employee_list.filter(Q(first_name__icontains=search_terms_array[term]) |
                                                         Q(last_name__icontains=search_terms_array[term]) |
                                                         Q(username__icontains=search_terms_array[term])).filter(is_base_profile_complete=True)
        else:
            employee_list = get_list_or_404(Employee, is_active=True, is_base_profile_complete=True)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(employee_list, request)
        serializer = EmployeeListSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def employee_location_list(request):
    """
    Returns employee location full list
    ---
    serializer: employees.serializers.EmployeeLocationListSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        location_list = get_list_or_404(Location)
        serializer = EmployeeLocationListSerializer(location_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def employee_position_list(request):
    """
    Returns employee position full list
    ---
    serializer: employees.serializers.EmployeePositionListSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        position_list = get_list_or_404(Position)
        serializer = EmployeePositionListSerializer(position_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def employee_role_list(request):
    """
    Returns employee role full list
    ---
    serializer: employees.serializers.EmployeeRoleListSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        role_list = get_list_or_404(Role)
        serializer = EmployeeRoleListSerializer(role_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def employee_image(request, employee_id):
    """
    Returns employee avatar
    ---
    response_serializer: employees.serializers.EmployeeAvatarSerializer
    parameters:
    - name: avatar
      required: true
      type: file
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=employee_id)
        serializer = EmployeeAvatarSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        employee = get_object_or_404(Employee, pk=employee_id)
        upload = request.FILES['image']
        employee.avatar.delete()
        employee.avatar = upload
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def employee_logout(request):
    """
    Logout employee
    ---
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if request.method == 'GET':
        employee = request.user
        try:
            devices = EmployeeDevice.objects.filter(username=employee)
            for device in devices:
                device.delete()
        except:
            pass
        logout(request)
        content = {'detail': config.USER_LOGOUT}
        return Response(content, status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def employee_register_device(request, employee_id):
    """
    Register employee device
    ---
    response_serializer: employees.serializers.EmployeeDeviceSerializer
    parameters:
    - name: android_device
      type: string
    - name: ios_device
      type: string
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
    - code: 500
      message: Internal Server Error
    """
    if request.method == 'POST':
        employee = get_object_or_404(Employee, pk=employee_id)
        device, created = EmployeeDevice.objects.get_or_create(username=employee)
        if 'android_device' in request.data:
            device.android_device = request.data['android_device']
        if 'ios_device' in request.data:
            device.ios_device = request.data['ios_device']
        device.save()
        serializer = EmployeeDeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
def employee_reset_password(request, employee_email):
    """
    This endpoint send an email to employee, with confirmation reset password url.
    ---
    responseMessages:
    - code: 404
      message: Not found
    - code: 406
      message: Request not acceptable
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, email=employee_email)

        # Generate random uuid and save in employee
        employee.generate_reset_password_code()

        # Send email with reset password confirmation url
        subject = config.EMPLOYEE_RESET_PASSWORD_CONFIRMATION_SUBJECT
        current_site = Site.objects.get_current()
        employee_reset_password_api = reverse('employees:employee_reset_password', args=[employee.email])
        url = current_site.domain + employee_reset_password_api + employee.reset_password_code
        message = config.EMPLOYEE_RESET_PASSWORD_CONFIRMATION_MESSAGE % (url)

        try:
            send_email = EmailMessage(subject, message, to=[employee.email])
            send_email.send()
        except Exception as e:
            print(e)
            content = {'detail': config.EMAIL_SERVICE_ERROR}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        content = {'detail': 'Confirmation email sent.',
                   'email': employee.email,
                   'reset_password_code': employee.reset_password_code}
        return Response(content, status=status.HTTP_200_OK)


@api_view(['GET', ])
@renderer_classes((StaticHTMLRenderer,))
def employee_reset_password_confirmation(request, employee_email, employee_uuid):
    """
    This endpoint reset employee with random password and send an email to employee with it.
    ---
    responseMessages:
    - code: 404
      message: Not found
    - code: 406
      message: Request not acceptable
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, email=employee_email, reset_password_code=employee_uuid)
        random_password = Employee.objects.make_random_password(length=4, allowed_chars='beatrx23456789')
        employee.set_password(random_password)
        employee.is_password_reset_required = True
        employee.save()

        # Send confirmation email
        subject = config.EMPLOYEE_RESET_PASSWORD_SUCCESSFULLY_SUBJECT
        message = config.EMPLOYEE_RESET_PASSWORD_SUCCESSFULLY_MESSAGE % (random_password)
        try:
            send_email = EmailMessage(subject, message, to=[employee.email])
            send_email.send()
        except Exception as e:
            print(e)
            data = "<h1>%s</h1>" % config.EMAIL_SERVICE_ERROR
            return Response(data)

        data = "<h1>%s</h1>" % config.USER_SUCCESSFULLY_RESET_PASSWORD
        return Response(data)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
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
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden.
    - code: 404
      message: Not found
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
            print(e)
            raise NotAcceptable(config.USER_DATA_IS_MISSING)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
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
    if request.method == 'POST':
        try:
            current_password = request.data['current_password']
            new_password = request.data['new_password']
        except Exception as e:
            print(e)
            raise NotAcceptable(config.USER_DATA_IS_MISSING)
        employee = get_object_or_404(Employee, pk=employee_id)
        if current_password == new_password:
            content = {'detail': config.PASSWORD_EQUAL}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif employee.check_password(current_password):
            employee.set_password(new_password)
            employee.reset_password_code = None
            employee.is_password_reset_required = False
            employee.save()
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            content = {'detail': config.WRONG_CURRENT_PASSWORD}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def top(request, kind, quantity):
    """
    Returns top {quantity} list, {kind} (total_score, level, last_month_score, current_month_score, last_year_score, current_year_score)
    ---
    serializer: employees.serializers.EmployeeTopListSerializer
    responseMessages:
    - code: 401
      message: Unauthorized. Authentication credentials were not provided. Invalid token.
    - code: 403
      message: Forbidden, authentication credentials were not provided
    - code: 404
      message: Not found
    - code: 500
      message: Internal server error, cannot resolve keyword into field.
    """
    try:
        employee_list_filtered = []
        if request.method == 'GET':
            employee_list = Employee.objects.filter(is_active=True, is_base_profile_complete=True).order_by('-' + kind)[:quantity]
            if kind == 'total_score':
                for employee in employee_list:
                    if employee.total_score > 0:
                        employee_list_filtered.append(employee)
                serializer = EmployeeTopTotalScoreList(employee_list_filtered, many=True)
            elif kind == 'level':
                for employee in employee_list:
                    if employee.level > 0:
                        employee_list_filtered.append(employee)
                serializer = EmployeeTopLevelList(employee_list_filtered, many=True)
            elif kind == 'current_month_score':
                for employee in employee_list:
                    if employee.current_month_score > 0:
                        employee_list_filtered.append(employee)
                serializer = EmployeeTopCurrentMonthList(employee_list_filtered, many=True)
            elif kind == 'current_year_score':
                for employee in employee_list:
                    if employee.current_year_score > 0:
                        employee_list_filtered.append(employee)
                serializer = EmployeeTopCurrentYearList(employee_list_filtered, many=True)
            elif kind == 'last_month_score':
                for employee in employee_list:
                    if employee.last_month_score > 0:
                        employee_list_filtered.append(employee)
                serializer = EmployeeTopLastMonthList(employee_list_filtered, many=True)
            elif kind == 'last_year_score':
                for employee in employee_list:
                    if employee.last_year_score > 0:
                        employee_list_filtered.append(employee)
                serializer = EmployeeTopLastYearList(employee_list_filtered, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        raise APIException(e)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Returns a token and user_id, for credentials provided.
        ---
        response_serializer: employees.serializers.EmployeeAuthenticationResponse
        responseMessages:
        - code: 404
          message: Not found
        - code: 500
          message: Unable to log in with provided credentials.
        parameters:
        - name: username
          required: true
          paramType: string
        - name: password
          required: true
          :paramType: string
        """
        try:
            # Filter username when email is used
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['username'] = request.POST['username'].split('@')[0]
            request.POST._mutable = mutable

            response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
            token = Token.objects.get(key=response.data['token'])
            employee = get_object_or_404(Employee, pk=token.user_id)
            return Response({'token': token.key,
                             'user_id': token.user_id,
                             'reset_password_code': employee.reset_password_code,
                             'is_base_profile_complete': employee.is_base_profile_complete,
                             'is_password_reset_required': employee.is_password_reset_required,
                             'is_staff': employee.is_staff})
        except Exception as e:
            print(e)
            raise NotAcceptable(config.USER_UNABLE_TO_LOG)
