from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


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
