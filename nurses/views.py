from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from patients.models import *
from .serializers import *
from .permissions import IsNurse
class GetProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,req):        
        Nurse = req.user
        serializer = NurseSerializer(Nurse)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetPatientsClinic(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req):
          try:
              Nurse = req.user
              PatientsReserv =   Reservation.objects.filter(clinic = Nurse.clinic, status='A' )
              print(PatientsReserv)
          except Reservation.DoesNotExist:
              return Response({"message": "clinic {Nurse.specialization}  and date sunday  is invalid!"}, status=status.HTTP_404_NOT_FOUND)
          serializer = ReservationsSerializer(PatientsReserv, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 