from common.utils import GenerateRandomPass, SendEmail
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import VerificationCode
from rest_framework import status
from .serializers import *
import os

@swagger_auto_schema(method='POST', request_body=CreateCodeSerializer)
@api_view(['POST'])
def CreateVerificationCode(req):
    code = GenerateRandomPass('', int(os.environ.get('VERIFICATION_CODE_LEN')))
    uri = req.build_absolute_uri()
    uri_arr = uri.split('/')
    uri_type = uri_arr[len(uri_arr) - 2] # change_email, register
    html_file = 'registration.html' if uri_type=='register' else 'change_email.html'

    serializer = CreateCodeSerializer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Invalid email", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    obj = VerificationCode.objects.filter(
        type=uri_type,
        email=serializer.data['email']
    )
    if obj.exists():
        obj.update(
            code=code,
            created_at=datetime.now()
        )
    else:
        data = VerificationCode.objects.create(
            type=uri_type,
            email=serializer.data['email'],
            code=code,
            created_at=datetime.now()
        )
    
    end_at=datetime.now()+timedelta(days=1)
    end_at=end_at.strftime("%Y/%m/%d, %I:%M:%S %p")

    SendEmail(
        userEmail=req.data['email'],
        code=code,
        expire_time=end_at,
        htmlFile=html_file
    )

    return Response({"message": "Success"}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='POST', request_body=ValidateCodeSerializer)
@api_view(['POST'])
def VerifyCode(req):
    serializer = ValidateCodeSerializer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Invalid code", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        obj = VerificationCode.objects.get(email=req.data['email'], code=req.data['code'])
    except VerificationCode.DoesNotExist:
        return Response({"message": "Wrong verification code, please make sure you entered the right code or requset another one!"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = GetCodeSerializer(obj, many=False)
    start_str=serializer.data['created_at']
    start_date = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S.%f')
    interval=datetime.now()- timedelta(days=1)
    if start_date < interval:
        return Response({"message": "Expired verification code, please requset another one!"}, status=status.HTTP_410_GONE)
    obj.delete()

    return Response({"message": "Valid code"}, status=status.HTTP_200_OK)

