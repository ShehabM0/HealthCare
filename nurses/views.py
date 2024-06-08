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
        return Response({"data": serializer.data, "count": len(serializer.data)}) 


class GetCurrentRoom(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req,room_id):
          try:
              room =   Room.objects.filter(id =room_id )
              bed =   Bed.objects.filter(room =room_id ,status='Empty')
          except room.DoesNotExist:
              return Response({"message": "room {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          except bed.DoesNotExist:
              return Response({"message": "bed {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          serializerRoom = RoomSerializer(room, many=True)
          serializerBed = BesSerializer(bed, many=True)
          return Response({"RoomData": serializerRoom.data,"BedDate":serializerBed.data}) 

class GetRoomsHistory(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req,room_id):
          try:
              room =   Room.objects.filter(id =room_id )
              bed =   Bed.objects.filter(room =room_id ,status='CheckOut' )
          except room.DoesNotExist:
              return Response({"message": "room {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          except bed.DoesNotExist:
              return Response({"message": "bed {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          serializerRoom = RoomSerializer(room, many=True)
          serializerBed = BesSerializer(bed, many=True)
          return Response({"RoomData": serializerRoom.data,"BedDate":serializerBed.data}) 


class GetBookedRoom(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req,room_id):
          try:
              room =   Room.objects.filter(id =room_id )
              bed =   Bed.objects.filter(room =room_id ,status='Booked' )
          except room.DoesNotExist:
              return Response({"message": "room {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          except bed.DoesNotExist:
              return Response({"message": "bed {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          serializerRoom = RoomSerializer(room, many=True)
          serializerBed = BesSerializer(bed, many=True)
          return Response({"RoomData": serializerRoom.data,"BedDate":serializerBed.data}) 
    

class UpdateRoom(APIView):
    permission_classes = [permissions.IsAuthenticated]

      
    def patch(self, req, bed_id):
        try:    
            bed =   Bed.objects.get(id =bed_id )
            room =   Room.objects.get( Room=bed.room )
        # except room.DoesNotExist:
        #     return Response({"message": "Room does not exist"},  status=status.HTTP_404_NOT_FOUND)
        except bed.DoesNotExist:
            return Response({"message": "Bed does not exist"},  status=status.HTTP_404_NOT_FOUND)
        
        serializer = updateRoomSerializer(data=req.data)
        if serializer.is_valid():
            
            room.save()
            bed.save()
            return Response({"message": "Room data updated successfully", "data" : RoomSerializer(room).data})
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)






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

    def get(self, req,Call_id):
          try:
              Nurse = req.user
              Call =   Calls.objects.filter(nurse = Nurse,id=Call_id)
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 
    
class GetCurrentCalls(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req):
          try:
              Nurse = req.user
              Call =   Calls.objects.filter(nurse = Nurse, status='Pending' )
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 
    
class GetCallsHistory(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req):
          try:
              Nurse = req.user
              Call =   Calls.objects.filter(nurse = Nurse, status='Done' )
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