from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from patients.models import User
from .serializers import *

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
    return Response({"message": "User not authenticated!"}, status=401)

@swagger_auto_schema(method='PATCH')
@api_view(['PATCH'])
def UpdateUser(req, pk=None):
    if not pk:
        user = req.user
        if not user.is_authenticated:
            return Response({"message": "User not authenticated!"}, status=401)
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
        return Response({"message": "User not authenticated!"}, status=401)
    
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

