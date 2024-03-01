from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from rest_framework.response import Response


class RegisterSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=1)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    date_of_birth = serializers.DateField()
    phone = serializers.CharField(max_length=15)
    address = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=30)
    confirm_password = serializers.CharField(max_length=30)
    gender = serializers.CharField(max_length=1)
    status = serializers.CharField(max_length=1)

    def validate( self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError("Password and Confirm Password does not match")
        if len(data['first_name']) < 2:
            raise ValidationError("First name must be at least 2 characters.")
        if len(data['last_name']) < 2:
            raise ValidationError("Last name must be at least 2 characters.")
        if len(data['password']) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        if len(data['phone']) < 11:
            raise ValidationError("Phone number must be at least 11 characters.")
        if data['phone'][0:2] != '01':
            raise ValidationError("Phone number must start with 01")
        return data