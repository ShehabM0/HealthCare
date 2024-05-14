from common.utils import GenerateRandomPass, SendEmail
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from django.db import IntegrityError
from patients.models import User
from datetime import datetime
from .models import Employee
from .serializers import *
import os

@swagger_auto_schema(method='POST', request_body=CreateEmployeeSerializer)
@api_view(['POST'])
def CreateEmployeeView(req):
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
            username=serializer.data['phone'],

            date_of_birth=serializer.data['date_of_birth'],
            address=serializer.data['address'],
            ssn=serializer.data['ssn'],
            insurance_number=serializer.data['insurance_number'],

            status=serializer.data['status'],
            gender=serializer.data['gender'],
            blood=serializer.data['blood'],

            password=user_pass,
            employee=None
        )
    except IntegrityError:
        return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CreateEmployeeSerializer(data=data)
    if not serializer.is_valid():
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    employee = Employee.objects.create(
        specialization=serializer.data['specialization'],
        salary=serializer.data['salary'],
        type=user_type,
        hired_at = datetime.now(),
        updated_at = datetime.now()
    )

    user.employee = employee
    user.save()
    SendEmail(
        userName=data['first_name'],
        userEmail=data['email'],
        userPass=user_pass,
        code=None,
        expire_time=None,
        htmlFile="hr_account_creation.html"
    )
    return Response({"message": "User created successfully, check your email."}, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='PATCH', request_body=UpdateEmployeeSerializer)
@api_view(['PATCH'])
def UpdateEmployeeView(req, pk=None):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "User doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)

    employee = user.employee
    if not employee:
        return Response({"message": "User isn't employee!"}, status=status.HTTP_404_NOT_FOUND)

    updated_employee = UpdateEmployeeSerializer(employee, data=req.data, partial=True)
    if not updated_employee.is_valid():
        return Response({"message": "Error updating Employee!", "data": updated_employee.errors})
    
    updated_employee.save()
    return Response({"message": "Success, Employee updated", "data": updated_employee.data})
    