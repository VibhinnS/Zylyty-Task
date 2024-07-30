from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from member.serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate, login

class UserRegisterView(APIView):
    def post(self, request):
        data = request.data
        if 'teapot' in data.get('username', '').lower():
            return Response(
                {'message': "I'm a teapot"},
                status=418
            )
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
