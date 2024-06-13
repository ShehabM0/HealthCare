from rest_framework.decorators import api_view, permission_classes
from common.utils import GenerateRandomPass, SendEmail
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status
from patients.models import User
from common.permissions import *
from datetime import datetime
from .models import Employee
from .serializers import *
import os

USER_TYPES = {
    'D': 'DOC_PASS_STR',
    'N': 'NURSE_PASS_STR',
    'H': 'HR_PASS_STR',
    'P': 'PH_PASS_STR',
    'HD': 'HD_PASS_STR',
    'HN': 'HN_PASS_STR'
}

@swagger_auto_schema(method='POST', request_body=CreateUserSerializer)
@swagger_auto_schema(method='PATCH', request_body=UpdateEmployeeSerializer)
@api_view(['POST', 'PATCH'])
@permission_classes([IsAuthenticated, IsHR])
def EmployeeView(req):
    if req.method == 'POST':
        return CreateEmployeeView(req)
    elif req.method == 'PATCH':
        return UpdateEmployeeView(req)

def CreateEmployeeView(req):
    data = req.data
    user_type = data['type'].upper()

    if user_type not in USER_TYPES.keys():
        return Response({
            "message": "Invalid user type!",
            "errors": "User type must be (D)octor, (N)urse, (H)uman resources, (P)harmacist, (H)ead (D)octor or (H)ead (N)urse."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user_type_str = os.environ.get(USER_TYPES[user_type])

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
    return Response({"message": "Employee created successfully, check your email."}, status=status.HTTP_201_CREATED)

def UpdateEmployeeView(req):
    employee = req.user

    updated_employee = UpdateEmployeeSerializer(employee, data=req.data, partial=True)
    if not updated_employee.is_valid():
        return Response({"message": "Error updating Employee!", "data": updated_employee.errors})
    
    updated_employee.save()
    return Response({"message": "Success, Employee updated", "data": updated_employee.data})
    
@swagger_auto_schema(method='PATCH', request_body=UpdateEmployeeSerializer)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsHR])
def UpdateEmployeeByIDView(req, pk):
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
