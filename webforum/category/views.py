import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer

ADMIN_API_KEY = os.getenv('ADMIN_API_KEY')

class CategoryListCreateView(APIView):
    def get(self, request):
        response = []
        categories = Category.objects.all()
        for category in categories:
            response.append(category.name)
        return Response(response, status=status.HTTP_200_OK)


    def post(self, request):
        json_data = []
        admin_api_key = request.headers.get('Token')
        if admin_api_key != ADMIN_API_KEY:
            return Response({"error":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        for category in (request.data['categories']):
            json_data.append({"name":category})

        serializer = CategorySerializer(data=json_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Category Created"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
