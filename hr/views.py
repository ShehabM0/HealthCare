from .helper import GenerateRandomPass, SendEmail
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.views import APIView
from django.db import IntegrityError
from patients.models import User
from .serializers import *
import os

@swagger_auto_schema(method='POST', request_body=CreateUserSerializer)
@api_view(['POST'])
def CreateUserView(req):
    # permission_classes = [permissions.AllowAny]

    data = req.data
    user_type = data['type'].upper()
    if user_type == 'D': user_type_str = os.environ.get('DOC_PASS_STR')
    elif user_type == 'N': user_type_str = os.environ.get('NURSE_PASS_STR')
    else: return Response({"message": "Invalid user type!", "errors": "User type must be (D)octor or (N)urse."}, status=status.HTTP_400_BAD_REQUEST)

    user_pass = GenerateRandomPass(user_type_str, int(os.environ.get('RANDOM_PASS_LEN')))
    
    serializer = CreateUserSerializer(data=data)
    if not serializer.is_valid():
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.create_user(
            email=serializer.data['email'],
            first_name=serializer.data['first_name'],
            last_name=serializer.data['last_name'],
            date_of_birth=serializer.data['date_of_birth'],
            address=serializer.data['address'],
            username = serializer.data['phone'],
            password = user_pass,
            status=serializer.data['status'],
            specialization=serializer.data['specialization'],
            type = user_type,
        )
        user.save()
        SendEmail(data['first_name'], data['email'], user_pass)
        return Response({"message": "User created successfully, check your email."}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def ListEmployeesView(req, type=None):
    if type: employees = User.objects.filter(type=type[0].upper())
    else: employees = User.objects.all()
    
    req_page_number = req.GET.get("page")
    if not req_page_number:
        serializer = UserSerializer(employees, many=True)
        return Response({"data": serializer.data, "count": len(serializer.data)})
    
    paginator = Paginator(employees, 10)
    page_number = int(req_page_number)
    page_obj = paginator.get_page(page_number)
    serializer = UserSerializer(page_obj, many=True)

    if page_number > paginator.num_pages:
        return Response({"data": [], "count": 0}, status=status.HTTP_404_NOT_FOUND)
    return Response({"data": serializer.data, "count": len(serializer.data)})

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def GetProfile(req, pk):
    try:
        data = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "User doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(data)
    return Response({"message": serializer.data})