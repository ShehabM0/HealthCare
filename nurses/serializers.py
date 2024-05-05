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
        fields = '__all__'
        depth = 1        

        