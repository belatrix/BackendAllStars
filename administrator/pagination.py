from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.response import Response


class AdministratorPagination(LimitOffsetPagination):
    default_limit = 50

    def get_paginated_response(self, data):
        return Response({
            "status": True,
            "code": status.HTTP_200_OK,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.count,
            'results': data
        })
