from django.db import IntegrityError
from django.http import JsonResponse
from .models import *
from django.http import JsonResponse
from .serializers import *
import os
from django.core.cache import cache
from rest_framework import serializers, status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from doctors.models import Clinic
from doctors.models import *




class Register_view(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.create_user(
                    email=serializer.data['email'],
                    first_name=serializer.data['first_name'],
                    last_name=serializer.data['last_name'],
                    date_of_birth=serializer.data['date_of_birth'],
                    address=serializer.data['address'],
                    password=serializer.data['password'],
                    type=serializer.data['type'],
                    status=serializer.data['status'],
                    username = serializer.data['phone'],
                    ssn = serializer.data['ssn'],
                    insurance_number = serializer.data['insurance_number'],
                    blood = serializer.data['blood']
                )
                user.save()
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class ReserveClinicView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=PreserveClinicSerializer)
    def post(self, request):
        serializer = PreserveClinicSerializer(data=request.data)
        if serializer.is_valid():
            
            user = request.user
            number_in_qeue = Reservations.objects.filter(clinic = serializer.data['clinic_id']).count() + 1
            
            reservation = Reservations(
                patient=user,
                clinic=Clinic.objects.get(id = serializer.data['clinic_id']),
                working_hour = WorkingHour.objects.get(id = serializer.data['working_hour_id']),
                number_in_qeue = number_in_qeue
            )
            reservation.save()
            return Response({"message": "Clinic preserved successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class ReservationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        reservations = Reservations.objects.filter(patient=user)
        serializer = ReservationsSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UploadMedicalRecord(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(request_body=UploadMedicalRecordSerializer)
    def post(self, request):
        serializer = UploadMedicalRecordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        medical_record = MedicalRecord(
            patient=request.user,
            file=request.data['file'],
            type=request.data['type']
        )
        medical_record.save()
        return Response({"message": "Medical record uploaded successfully"}, status=status.HTTP_200_OK)
