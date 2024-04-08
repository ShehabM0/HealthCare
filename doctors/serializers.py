from .models import *

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
    status = serializers.CharField(max_length=1, required=True)

    def validate(self, data):
        if data['status'] not in ['A', 'C']:
            raise serializers.ValidationError({"status": "Invalid status"})
        return data