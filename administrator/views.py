from activities.models import Message
from categories.models import Category, Keyword
from constance import config
from employees.models import Employee, Location, Position, Role
from events.models import Event, EventActivity
from stars.models import Badge
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CategorySerializer, KeywordSerializer, BadgeSerializer
from .serializers import EmployeeSerializer, EmployeeTopSerializer
from .serializers import LocationSerializer, PositionSerializer, RoleSerializer
from .serializers import EventSerializer, EventActivitySerializer
from .serializers import MessageSerializer, SiteInfoSerializer
from .pagination import AdministratorPagination


class BadgeList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, format=None):
        """
        List all badges
        ---
        serializer: administrator.serializers.BadgeSerializer
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        """
        badges = get_list_or_404(Badge)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(badges, request)
                serializer = BadgeSerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = BadgeSerializer(badges, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

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
        ---
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        """
        categories = get_list_or_404(Category)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(categories, request)
                serializer = CategorySerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

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


class EmployeeList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, format=None):
        """
        List all employees
        ---
        serializer: administrator.serializers.EmployeeSerializer
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        """
        employees = get_list_or_404(Employee)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(employees, request)
                serializer = EmployeeSerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeTopList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, kind, format=None):
        """
        List all employees
        ---
        serializer: administrator.serializers.EmployeeSerializer
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        - name: quantity
          required: false
          type: string
          paramType: query
        """
        employee_list = Employee.objects.filter(is_active=True, is_base_profile_complete=True).order_by('-' + kind)
        if request.GET.get('quantity'):
            try:
                quantity = request.GET.get('quantity')
                employee_list = employee_list[:quantity]
            except Exception as e:
                raise APIException(e)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(employee_list, request)
                serializer = EmployeeTopSerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = EmployeeTopSerializer(employee_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class EventList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, format=None):
        """
        List all events
        ---
        serializer: administrator.serializers.EventSerializer
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        """
        events = get_list_or_404(Event)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(events, request)
                serializer = EventSerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create new event
        ---
        serializer: administrator.serializers.EventSerializer
        """
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, event_id, format=None):
        """
        Get event details
        ---
        serializer: administrator.serializers.EventSerializer
        """
        event = get_object_or_404(Event, pk=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, event_id, format=None):
        """
        Edit event
        ---
        serializer: administrator.serializers.EventSerializer
        """
        event = get_object_or_404(Category, pk=event_id)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id, format=None):
        """
        Delete event (inactive event, you should edit is_active attribute to revert this change)
        ---
        serializer: administrator.serializers.EventSerializer
        """
        event = get_object_or_404(Event, pk=event_id)
        event.is_active = False
        event.save()
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class EventActivityList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, event_id, format=None):
        """
        List all activities for an event
        ---
        serializer: administrator.serializers.EventActivitySerializer
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        """
        event = get_object_or_404(Event, pk=event_id)
        activities = EventActivity.objects.filter(event=event)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(activities, request)
                serializer = EventActivitySerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = EventActivitySerializer(activities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class EventActivityDetail(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, event_id, news_id, format=None):
        """
        Get event activity detail
        ---
        serializer: administrator.serializers.EventActivitySerializer
        """
        event = get_object_or_404(Event, pk=event_id)
        activity = get_object_or_404(EventActivity, event=event, pk=news_id)
        serializer = EventActivitySerializer(activity)
        return Response(serializer.data)

    def delete(self, request, event_id, news_id, format=None):
        """
        Delete event activity (you cannot revert this change)
        """
        event = get_object_or_404(Event, pk=event_id)
        activity = get_object_or_404(EventActivity, event=event, pk=news_id)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        - name: pagination
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

        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(keywords, request)
                serializer = KeywordSerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = KeywordSerializer(keywords, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

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


class LocationList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, format=None):
        """
        List all employee positions
        ---
        serializer: administrator.serializers.LocationSerializer
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        """
        locations = get_list_or_404(Location)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(locations, request)
                serializer = LocationSerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = LocationSerializer(locations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create new location
        ---
        serializer: administrator.serializers.LocationSerializer
        """
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetail(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, location_id, format=None):
        """
        Get location detail
        """
        location = get_object_or_404(Location, pk=location_id)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def put(self, request, location_id, format=None):
        """
        Edit location
        ---
        serializer: administrator.serializers.LocationSerializer
        """
        location = get_object_or_404(Location, pk=location_id)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, location_id, format=None):
        """
        Deactivate location, you should edit is_active attribute to revert this change
        ---
        serializer: administrator.serializers.LocationSerializer
        """
        location = get_object_or_404(Location, pk=location_id)
        location.is_active = False
        location.save()
        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class MessageList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, format=None):
        """
        List all messages
        ---
        serializer: administrator.serializers.MessageSerializer
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        """
        messages = get_list_or_404(Message)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(messages, request)
                serializer = MessageSerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class MessageDetail(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, message_id, format=None):
        """
        Get message detail
        ---
        serializer: administrator.serializers.MessageSerializer
        """
        message = get_object_or_404(Message, pk=message_id)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def delete(self, request, message_id, format=None):
        """
        Delete message (you cannot revert this change)
        ---
        serializer: administrator.serializers.MessageSerializer
        """
        message = get_object_or_404(Event, pk=message_id)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageListFromEmployee(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, employee_id, format=None):
        """
        List all messages from employee
        ---
        serializer: administrator.serializers.MessageSerializer
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        """
        employee = get_object_or_404(Employee, pk=employee_id)
        messages = get_list_or_404(Message, from_user=employee)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(messages, request)
                serializer = MessageSerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class PositionList(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, format=None):
        """
        List all employee positions
        ---
        serializer: administrator.serializers.PositionSerializer
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        """
        positions = get_list_or_404(Position)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(positions, request)
                serializer = PositionSerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PositionSerializer(positions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

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
        return Response(serializer.data)

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


class RoleList(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, format=None):
        """
        List all roles
        ---
        serializer: administrator.serializers.RoleSerializer
        parameters:
        - name: pagination
          required: false
          type: string
          paramType: query
        """
        roles = get_list_or_404(Role)
        if request.GET.get('pagination'):
            pagination = request.GET.get('pagination')
            if pagination == 'true':
                paginator = AdministratorPagination()
                results = paginator.paginate_queryset(roles, request)
                serializer = RoleSerializer(results, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = RoleSerializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create new Role
        ---
        serializer: administrator.serializers.RoleSerializer
        """
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleDetail(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, role_id, format=None):
        """
        Get role detail
        ---
        serializer: administrator.serializers.RoleSerializer
        """
        role = get_object_or_404(Role, pk=role_id)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    def put(self, request, role_id, format=None):
        """
        Edit role
        ---
        serializer: administrator.serializers.RoleSerializer
        """
        role = get_object_or_404(Role, pk=role_id)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, role_id, format=None):
        """
        Delete role, you should edit is_active to revert this change.
        ---
        serializer: administrator.serializers.RoleSerializer
        """
        role = get_object_or_404(Role, pk=role_id)
        role.is_active = False
        role.save()
        serializer = RoleSerializer(role)
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
        elif kind == 'event':
            kind = get_object_or_404(Event, pk=id)
        elif kind == 'keyword':
            kind = get_object_or_404(Keyword, pk=id)
        elif kind == 'location':
            kind = get_object_or_404(Location, pk=id)
        elif kind == 'position':
            kind = get_object_or_404(Position, pk=id)
        elif kind == 'role':
            kind = get_object_or_404(Role, pk=id)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        kind.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SiteInfoDetail(APIView):

    def get(self, request, format=None):
        """
        Get site info
        ---
        serializer: administrator.serializers.SiteInfoSerializer
        """
        email_domain = settings.EMAIL_DOMAIN_LIST[0]
        current_site = Site.objects.get_current()
        version = config.VERSION

        data = {'site': current_site.domain,
                'email_domain': email_domain,
                'backend_version': version}

        serializer = SiteInfoSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
