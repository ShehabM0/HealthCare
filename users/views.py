from verification_code.models import VerificationCode
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from common.utils import SendEmail
from rest_framework import status
from patients.models import User
from verification_code.serializers import GetCodeSerializer
from .serializers import *
import os

# Create your views here.
@swagger_auto_schema(method='GET')
@api_view(['GET'])
def ListUsers(req, type=None):
    if type: users = User.objects.filter(type=type[0].upper())
    else: users = User.objects.all()
    
    req_page_number = req.GET.get("page")
    if not req_page_number:
        serializer = UserSerializer(users, many=True)
        return Response({"data": serializer.data, "count": len(serializer.data)})
    
    paginator = Paginator(users, 10)
    page_number = int(req_page_number)
    page_obj = paginator.get_page(page_number)
    serializer = UserSerializer(page_obj, many=True)

    if page_number > paginator.num_pages:
        return Response({"data": [], "count": 0}, status=status.HTTP_404_NOT_FOUND)
    return Response({"data": serializer.data, "count": len(serializer.data)})

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def GetUser(req, pk):
    try:
        data = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "User doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(data)
    return Response({"message": serializer.data})

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def GetCurrentUser(req):
    user = req.user
    if user.is_authenticated:
        serializer = UserSerializer(user)
        return Response({"message": "Success", "data": serializer.data})
    return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(method='PATCH')
@api_view(['PATCH'])
def UpdateUser(req, pk=None):
    if not pk:
        user = req.user
        if not user.is_authenticated:
            return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"message": "User doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user)
    user_id = serializer.data['id']
    serializer = UpdateUserSerializer(user, data=req.data, partial=True, context={'user_id': user_id})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Success, User updated", "data": serializer.data})
    return Response({"message": "Error updating User!", "data": serializer.errors})

@swagger_auto_schema(method='PATCH', request_body=UpdateEmailSerializer)
@api_view(['PATCH'])
def UpdateEmail(req):
    user = req.user
    if not user.is_authenticated:
        return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = UserSerializer(user)
    user_id = serializer.data['id']

    serializer = UpdateEmailSerializer(user, data=req.data, partial=True, context={'user_id': user_id})
    if not serializer.is_valid():
        return Response({"message": "Error updating Email!", "data": serializer.errors})
    
    serializer.save()
    return Response({"message": "Success, Email updated", "data": serializer.data})

@swagger_auto_schema(method='PATCH', request_body=UpdatePasswordSerializer)
@api_view(['PATCH'])
def UpdatePassword(req):
    user = req.user
    old_password = req.data['old_password']
    new_password = req.data['password']
    confirm_new_password = req.data['confirm_password']
    
    serializer = UpdatePasswordSerializer(data=req.data, partial=True)
    if not serializer.is_valid():
        return Response({"message": "Error updating Password!", "data": serializer.errors})

    user = authenticate(username=user.username, password=old_password)
    if not user:
        return Response({"message": "Wrong password, try again!"}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({"message": "Success, Password updated", "data": serializer.data})

@swagger_auto_schema(method='POST', request_body=VerifyEmailSerializer)
@api_view(['POST'])
def ForgotPassword(req):
    user = req.user
    if not user.is_authenticated:
        return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = UserSerializer(user)
    user_id = serializer.data['id']

    serializer = VerifyEmailSerializer(user, data=req.data, context={'user_id': user_id})
    if not serializer.is_valid():
        return Response({"message": "Error verifying Email", "data": serializer.errors}, status=status.HTTP_404_NOT_FOUND)
    

    redirect_url=req.GET.get("redirect_url", "")
    html_file="forgot_password.html"
    end_at=datetime.now()+timedelta(hours=1)
    end_at=end_at.strftime("%Y/%m/%d, %I:%M:%S %p")
    token = get_random_string(int(os.environ.get('FORGOT_PASSWORD_TOKEN_LEN')))

    obj = VerificationCode.objects.filter(
        type='forgot-password',
        email=serializer.data['email']
    )
    if obj.exists():
        obj.update(
            code=token,
            created_at=datetime.now()
        )
    else:
        VerificationCode.objects.create(
            type='forgot-password',
            email=serializer.data['email'],
            code=token,
            created_at=datetime.now()
        )

    SendEmail(
        userEmail=serializer.data['email'],
        code=token,
        redirect_url=redirect_url,
        expire_time=end_at,
        htmlFile=html_file
    )

    return Response({"message": "Email sent, Check your email to reset your password."}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='POST', request_body=ResetPasswordSerializer)
@api_view(['POST'])
def ResetPassword(req, token):
    user = req.user
    if not user.is_authenticated:
        return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        obj = VerificationCode.objects.get(code=token)
    except VerificationCode.DoesNotExist:
        return Response({"message": "Wrong verification code, please make sure you entered the right code or requset another one!"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = GetCodeSerializer(obj, many=False)
    start_str=serializer.data['created_at']
    start_date=datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S.%f')
    interval=datetime.now()- timedelta(hours=1)
    if start_date < interval:
        return Response({"message": "Expired token link, please requset another one!"}, status=status.HTTP_410_GONE)
    obj.delete()

    serializer = ResetPasswordSerializer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Invalid Password!", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    user_pass = serializer.data['password']
    user.set_password(user_pass)
    user.save()
    return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    

@swagger_auto_schema(method='DELETE')
@api_view(['DELETE'])
def DeleteUser(req, pk=None):
    if not pk:
        user = req.user
        if not user.is_authenticated:
            return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"message": "User doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response({"message": "User Deleted."})

