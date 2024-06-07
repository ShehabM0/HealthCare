from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from patients.models import *
from .serializers import *
from .permissions import IsNurse
from drf_yasg.utils import swagger_auto_schema




class GetProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,req):        
        Nurse = req.user
        serializer = NurseSerializer(Nurse)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetPatientsClinic(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req):
          try:
              Nurse = req.user
              PatientsReserv =   Reservation.objects.filter(clinic = Nurse.clinic, status='A')
          except Reservation.DoesNotExist:
              return Response({"message": "clinic {Nurse.specialization}  and date sunday  is invalid!"}, status=status.HTTP_404_NOT_FOUND)
          serializer = ReservationsSerializer(PatientsReserv, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 


################################## Room 
class GetAllRooms(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req):
        
        room = Room.objects.all()
        serializer = RoomSerializer(room, many=True)
        return Response({"data": serializer.data}) 


class GetRoom(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req,room_id):
          try:
              room =   Room.objects.filter(id =room_id )
              bed =   Bed.objects.filter(room =room_id )
          except room.DoesNotExist:
              return Response({"message": "room {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          except bed.DoesNotExist:
              return Response({"message": "bed {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          serializerRoom = RoomSerializer(room, many=True)
          serializerBed = BesSerializer(bed, many=True)
          return Response({"RoomData": serializerRoom.data,"BedDate":serializerBed.data}) 



# class CreateRoom(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, req):
#           serializer = PreserveCallSerializer(data=req.data)
#           if serializer.is_valid():
              
#               Nurse = req.user
#               Call =   Calls.objects.filter(nurse = Nurse, status='P' )
#               return Response({"message": "Call Created successfully"}, status=status.HTTP_200_OK)
#           else:
#             return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)






########################################Calls

class GetAllCalls(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req):
          try:
              Call =   Calls.objects.all()
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 


class GetCalls(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req):
          try:
              Nurse = req.user
              Call =   Calls.objects.filter(nurse = Nurse, status='Pending' )
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 
    


    
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