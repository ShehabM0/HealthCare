from django.db import IntegrityError
from django.http import JsonResponse
from .models import *
from django.http import JsonResponse
from .serializers import *
import os
from django.core.cache import cache
from rest_framework import serializers, status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView




class Register_view(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.create_user(
                    email=serializer.data['email'],
                    first_name=serializer.data['first_name'],
                    last_name=serializer.data['last_name'],
                    date_of_birth=serializer.data['date_of_birth'],
                    address=serializer.data['address'],
                    password=serializer.data['password'],
                    type=serializer.data['type'],
                    status=serializer.data['status'],
                    username = serializer.data['phone'],
                )
                user.save()
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
