from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from rest_framework.response import Response
from patients.models import *


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'number_in_qeue', 'type', 'patient']
        depth = 1        

# class CallsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Calls
#         fields ='__all__'
#         depth = 1      

# class RoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields ='__all__'
#         depth = 1        

# class PreserveCallSerializer(serializers.Serializer):
#     room_id = serializers.IntegerField()
#     patient_id = serializers.IntegerField()
#     doctor_id = serializers.IntegerField()
#     nurse_id = serializers.IntegerField()

#     def validate(self,data):
        
#         if not Room.objects.filter(id=data['room_id']).exists():
#             raise ValidationError({"room_id": "room does not exist"})
#         if not Employee.objects.filter(id=data['patient_id']).exists():
#             raise ValidationError({"patient_id": "patient does not exist"})
#         if not Employee.objects.filter(id=data['doctor_id']).exists():
#             raise ValidationError({"doctor_id": "doctor does not exist"})
#         if not Employee.objects.filter(id=data['nurse_id']).exists():
#             raise ValidationError({"nurse_id": "nurse does not exist"})
        
#         if data['status'] not in ['Pending', 'Done']:
#             raise ValidationError("Invalid status. Must be Pending, or Done.")
        
#         if data['type'] not in ['Surgery', 'inPatient Treatment']:
#             raise ValidationError("Invalid type. Must be Surgery, or inPatient Treatment.")
        
#         if len(data['room']) < 1:
#             raise ValidationError({"room": "room name must be at least 1 characters."})
#         if len(data['disease']) < 2:
#             raise ValidationError({"disease": "disease name must be at least 2 characters."})
#         if len(data['treatment']) < 2:
#             raise ValidationError({"treatment": "treatment name must be at least 2 characters."})
#         if len(data['descrption']) < 2:
#             raise ValidationError({"descrption": "descrption must be at least 2 characters."})                
#         return data
