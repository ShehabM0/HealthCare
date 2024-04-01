from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from rest_framework.response import Response


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30)
    confirm_password = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=15)

    def validate( self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError({"confirm_password": "Password and Confirm Password does not match"})
        if len(data['first_name']) < 2:
            raise ValidationError({"first_name": "First name must be at least 2 characters."})
        if len(data['last_name']) < 2:
            raise ValidationError({"last_name": "Last name must be at least 2 characters."})
        if len(data['password']) < 8:
            raise ValidationError({"password": "Password must be at least 8 characters."})
        if len(data['phone']) < 11:
            raise ValidationError({"phone": "Phone number must be at least 11 characters."})
        if data['phone'][0:2] != '01':
            raise ValidationError({"phone": "Phone number must start with 01"})
        return data
    
class PreserveClinicSerializer(serializers.Serializer):
    clinic_id = serializers.IntegerField()
    working_hour_id = serializers.IntegerField()

class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = '__all__'
        depth = 1

class UploadMedicalRecordSerializer(serializers.Serializer):
    file = serializers.FileField()
    type = serializers.CharField(max_length=1)

    def validate (self, data):
        if data['type'] not in ['P', 'R', 'I', 'A']:
            raise ValidationError("Invalid type")
        return data
    
class UpdateDeleteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
'''
date_of_birth = serializers.DateField()
type = serializers.CharField(max_length=1)
address = serializers.CharField(max_length=100)
gender = serializers.CharField(max_length=1)
status = serializers.CharField(max_length=1)
blood = serializers.CharField(max_length=3)
ssn = serializers.CharField(min_length=14)
insurance_number = serializers.CharField(min_length=9)

if len(data['ssn']) != 14:
    raise ValidationError("Social Security number must be 14 digits.")
if len(data['insurance_number']) != 9:
    raise ValidationError("Insurance number must be 9 digits.")
''' 


