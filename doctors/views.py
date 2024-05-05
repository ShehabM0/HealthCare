from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from .permissions import IsDoctor
from common.utils import get_status_word


class ListClinicsView(generics.ListCreateAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    

class ClinicView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer

class AddClinicView(generics.CreateAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    
class AddWorkingHourView(generics.CreateAPIView):
    queryset = WorkingHour.objects.all()
    serializer_class = AddWorkingHourSerializer

class WorkingHoursView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer


class ListWorkingHoursView(generics.ListAPIView):
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer


    
class ListAllClinics(APIView):
    def get(self, request):
        clinics = Clinic.objects.all()
        response = []
        for clinic in clinics:
            clinic_doctor = User.objects.filter(clinic=clinic, type='D').first()
            serializer = ClinicSerializer(clinic).data
            serializer['doctor'] = DoctorSerializer(clinic_doctor).data
            response.append(serializer)
        return Response(response)
    
class GetClinicWorkingHours(APIView):
    def get(self,request, clinic_id):
        working_hours = WorkingHour.objects.filter(clinic_id=clinic_id, day__gte=datetime.now())
        serializer = WorkingHourSerializer(working_hours, many=True)
        return Response(serializer.data)

class UpdateClinicStatus(APIView):
    @swagger_auto_schema(request_body=updateClinicStatusSerializer)
    def patch(self, request, clinic_id):
        try:
            clinic = Clinic.objects.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Response({"message": "Clinic does not exist"}, status=404)
        serializer = updateClinicStatusSerializer(data=request.data)
        if serializer.is_valid():
            clinic.status = serializer.data.get('status', clinic.status)
            clinic.price = serializer.data.get('price', clinic.price)
            clinic.save()
            return Response({"message": "Clinic data updated successfully", "data" : ClinicSerializer(clinic).data})
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)
    

class DoctorCasesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        working_hour = WorkingHour.objects.filter(clinic_id=user.clinic, day__gte=datetime.now()).first()
        cases = Reservation.objects.filter(clinic = user.clinic, status='A' , working_hour=working_hour)
        serializer = CaseSerializer(cases, many=True)
        return Response({"data": serializer.data , "count": cases.count()})
    

class UserDetails(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get(self, request, id):
        try:
            user = User.objects.get(id=id, type='P')
            # status_types is like [('',''),('','')]
            user.status = get_status_word(user.status, User.STATUS_TYPES)
            user.gender = get_status_word(user.gender, User.STATUS_TYPES)
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=404)
        serializer = PatientSerializer(user)
        return Response(serializer.data)
    
    
class PatientMedicalRecordView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get(self, request, id):
        user = User.objects.filter(id=id, type='P').first()
        medicalRecords = MedicalRecord.objects.filter(patient=user)
        for file in medicalRecords:
            file.type = get_status_word(file.type, MedicalRecord.FILE_TYPES)
        serializer = MedicalRecordSerializer(medicalRecords, many=True)
        return Response({"data" : serializer.data, "count": medicalRecords.count()})