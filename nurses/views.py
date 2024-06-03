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
              PatientsReserv =   Reservation.objects.filter(clinic = Nurse.clinic, status='A'|'B' )
          except Reservation.DoesNotExist:
              return Response({"message": "clinic {Nurse.specialization}  and date sunday  is invalid!"}, status=status.HTTP_404_NOT_FOUND)
          serializer = ReservationsSerializer(PatientsReserv, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 


# class GetRoom(APIView):
#     permission_classes = [permissions.IsAuthenticated,IsNurse]

#     def get(self, req):
#           try:
#               roomName = req.data
#               room =   room.objects.filter(name =roomName )
#           except room.DoesNotExist:
#               return Response({"message": "room {roomName} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
#           serializer = RoomSerializer(room, many=True)
#           return Response({"data": serializer.data}) 




# class GetCalls(APIView):
#     permission_classes = [permissions.IsAuthenticated,IsNurse]

#     def get(self, req):
#           try:
#               Nurse = req.user
#               Call =   Calls.objects.filter(nurse = Nurse, status='P' )
#           except Call.DoesNotExist:
#               return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
#           serializer = CallsSerializer(Call, many=True)
#           return Response({"data": serializer.data, "count": len(serializer.data)}) 
    


    
# class CreateCalls(APIView):
#     permission_classes = [permissions.IsAuthenticated,IsNurse]

#     def post(self, req):
#           serializer = PreserveCallSerializer(data=req.data)
#           if serializer.is_valid():
              
#               Nurse = req.user
#               Call =   Calls.objects.filter(nurse = Nurse, status='P' )
#               return Response({"message": "Call Created successfully"}, status=status.HTTP_200_OK)
#           else:
#             return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)