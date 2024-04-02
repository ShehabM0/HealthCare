from django.shortcuts import render
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.views import APIView
from django.db import IntegrityError
from patients.models import *
from .serializers import *
import os
from datetime import date

class GetProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,req):
          try:
              Nurse = req.user
          except User.DoesNotExist:
              return Response({"message": "Nurse with ID : {Nurse.email} doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)
          except not Nurse.is_authenticated:
              return Response({"message": "User not authenticated!"}, status=401)
          serializer = NurseSerializer(Nurse)
          return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetPatientsClinic(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req):
          try:
              PatientsReserv =  Reservations.objects.filter(clinic=req.clinic , working_hour=req.date)
          except Reservations.DoesNotExist:
              return Response({"message": "clinic {req.clinic}  and date {req.date}  is invalid!"}, status=status.HTTP_404_NOT_FOUND)
          if PatientsReserv.acount==0 :
               return Response({"message": "there is no clinic {req.clinic}  on  date {req.date} !"}, status=status.HTTP_404_NOT_FOUND)
          serializer = ReservationsSerializer(PatientsReserv)
          return Response({"data": serializer.data, "count": len(serializer.data)})

