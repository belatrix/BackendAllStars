from .models import Subcategory
from .serializers import SubCategoryListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def subcategories_list(request, category_id):
    if request.method == 'GET':
        subcategories = Subcategory.objects.filter(category=category_id)
        serializer = SubCategoryListSerializer(subcategories, many=True)
        return  Response(serializer.data, status=status.HTTP_200_OK)


