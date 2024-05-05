from .models import *
from patients.models import *

from rest_framework import serializers

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AddWorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = '__all__'

class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = '__all__'



class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'id']

class updateClinicStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=1, required=False)
    price = serializers.FloatField(required=False)

    def validate(self, data):
        if 'status' not in data and 'price' not in data:
            raise serializers.ValidationError({"message": "At least one of 'price' or 'status' must be provided"})
        
        if 'status' in data and data['status'] not in ['A', 'C']:
            raise serializers.ValidationError({"status": "Invalid status"})
        
        if 'price' in data and data['price'] is not None and data['price'] < 0:
            raise serializers.ValidationError({"price": "Invalid price"})
        
        return data
    

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'blood', 'gender', 'status']


class CaseSerializer(serializers.ModelSerializer):
    patient = DoctorSerializer()
    class Meta:
        model = Reservation
        fields = ['id', 'status', 'type', 'patient']
        depth=1


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        exclude = ['patient']

