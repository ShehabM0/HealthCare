from common.utils import GenerateRandomPass, SendEmail
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.response import Response
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
    elif user_type == 'H': user_type_str = os.environ.get('HR_PASS_STR')
    else: return Response({"message": "Invalid user type!", "errors": "User type must be (D)octor, (N)urse or (H)uman resources."}, status=status.HTTP_400_BAD_REQUEST)

    user_pass = GenerateRandomPass(user_type_str, int(os.environ.get('RANDOM_PASS_LEN')))
    
    serializer = CreateUserSerializer(data=data)
    if not serializer.is_valid():
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.create_user(
            email=serializer.data['email'],
            first_name=serializer.data['first_name'],
            last_name=serializer.data['last_name'],
            username = serializer.data['phone'],

            date_of_birth=serializer.data['date_of_birth'],
            address=serializer.data['address'],
            ssn = serializer.data['ssn'],
            insurance_number = serializer.data['insurance_number'],

            status=serializer.data['status'],
            specialization=serializer.data['specialization'],
            gender=serializer.data['gender'],
            blood = serializer.data['blood'],

            password = user_pass,
            type = user_type,
        )
        user.save()
        SendEmail(
            userName=data['first_name'],
            userEmail=data['email'],
            userPass=user_pass,
            code=None,
            htmlFile="hr_account_creation.html"
        )
        return Response({"message": "User created successfully, check your email."}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

