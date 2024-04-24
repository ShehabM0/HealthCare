from django.db import IntegrityError
from django.db.models import Q
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
from rest_framework import generics


class ValidateRegister_view(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user_exist = User.objects.filter(Q(username=serializer.data['phone']) | Q(email=serializer.data['email'])).exists()
        if user_exist:
            return Response({"message": "User already exists"}, status=status.HTTP_409_CONFLICT)
        return Response({"message": "Valid data"}, status=status.HTTP_200_OK)


class Register_view(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.create_user(
                    first_name=serializer.data['first_name'],
                    last_name=serializer.data['last_name'],
                    email=serializer.data['email'],
                    password=serializer.data['password'],
                    username = serializer.data['phone'],
                )
                user.save()
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"message": "User already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class ReserveClinicView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=PreserveClinicSerializer)
    def post(self, request):
        serializer = PreserveClinicSerializer(data=request.data)
        if serializer.is_valid():
            
            user = request.user
            number_in_qeue = Reservation.objects.filter(clinic = serializer.data['clinic_id'], working_hour=serializer.data['working_hour_id']).count() + 1
            if Reservation.objects.filter(clinic=serializer.data['clinic_id'], working_hour=serializer.data['working_hour_id'], patient=request.user.pk).exists():
                raise ValidationError({"clinic_id": "This clinic is already reserved"})
            clinic = Clinic.objects.get(id = serializer.data['clinic_id'])
            reservation = Reservation(
                patient=user,
                clinic=clinic,
                working_hour = WorkingHour.objects.get(id = serializer.data['working_hour_id']),
                number_in_qeue = number_in_qeue,
                price = clinic.price
            )
            reservation.save()
            return Response({"message": "Clinic preserved successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

        

class GetClinicQeueView(APIView):
    def get(self, request, clinic_id, working_hour_id):
        return Response({"number in qeue": Reservation.objects.filter(clinic = clinic_id, working_hour=working_hour_id).count() + 1}, status=status.HTTP_200_OK)
        

class ReservationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        reservations = Reservation.objects.filter(patient=user)
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
    
    def get(self, request):
        medical_records = MedicalRecord.objects.filter(patient=request.user)
        serializer = MedicalRecordSerializer(medical_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateReservationStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(request_body=UpdateReservationStatusSerializer)
    def patch(self, request, reservation_id):
        serializer = UpdateReservationStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.status = serializer.data['status']
        reservation.save()
        return Response({"message": "Reservation status updated successfully", "data" : ReservationsSerializer(reservation).data}, status=status.HTTP_200_OK)
    
    def get(self,request,reservation_id):
        permission_classes = [permissions.IsAuthenticated]
        try:
            reservation = Reservation.objects.get(id=reservation_id, patient=request.user)
            serializer = ReservationsSerializer(reservation)
            return Response({'data' : serializer.data})
        except Reservation.DoesNotExist:
            return Response({"message": "Reservation does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id, patient=request.user)
            reservation.delete()
            reservations = Reservation.objects.filter(clinic=reservation.clinic, working_hour=reservation.working_hour, number_in_qeue__gt=reservation.number_in_qeue)
            for res in reservations:
                if res.number_in_qeue > 1:
                    res.number_in_qeue -= 1
                    res.save()
            return Response({"message": "Reservation deleted successfully"}, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({"message": "Reservation does not exist"}, status=status.HTTP_404_NOT_FOUND)


class ReservationsHistory(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        reservations = Reservation.objects.filter(patient=request.user)
        serializer = ReservationsSerializer(reservations, many=True)
        return Response({'data' : serializer.data})