from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from patients.models import *
from .serializers import *
from .permissions import IsNurse
from drf_yasg.utils import swagger_auto_schema


class GetUserId(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,req):        
        Users = User.objects.all()
        serializer = UserIdSerializer(Users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetProfile(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self,req):        
        Nurse = req.user
        serializer = NurseSerializer(Nurse, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetPatientsClinic(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req):
          try:
              Nurse = req.user
              PatientsReserv =   Reservation.objects.filter(clinic = Nurse.clinic, status='A')
          except Reservation.DoesNotExist:
              return Response({"message": "clinic {Nurse.specialization}  and date sunday  is invalid!"}, status=status.HTTP_404_NOT_FOUND)
          serializer = ReservationsSerializer(PatientsReserv, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 

class UserDetails(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNurse]

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=404)
        serializer = PatientSerializer(user)


        return Response(serializer.data)
    


################################## Room 



class GetAllRooms(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req):
        
        room = Room.objects.all()
        serializer = RoomSerializer(room, many=True)
        return Response({"data": serializer.data, "count": len(serializer.data)}) 


class GetCurrentRoom(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req,room_id):
          try:
              room =   Room.objects.filter(id =room_id )
              bed =   Bed.objects.filter(room =room_id ,status='Empty')
          except room.DoesNotExist:
              return Response({"message": "room {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          except bed.DoesNotExist:
              return Response({"message": "bed {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          serializerRoom = RoomSerializer(room, many=True)
          serializerBed = BedSerializer(bed, many=True)
          return Response({"RoomData": serializerRoom.data,"BedDate":serializerBed.data}) 

class GetRoomsHistory(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req,room_id):
          try:
              room =   Room.objects.filter(id =room_id )
              bed =   Bed.objects.filter(room =room_id ,status='CheckOut' )
          except room.DoesNotExist:
              return Response({"message": "room {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          except bed.DoesNotExist:
              return Response({"message": "bed {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          serializerRoom = RoomSerializer(room, many=True)
          serializerBed = BedSerializer(bed, many=True)
          return Response({"RoomData": serializerRoom.data,"BedDate":serializerBed.data}) 


class GetBookedRoom(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req,room_id):
          try:
              room =   Room.objects.filter(id =room_id )
              bed =   Bed.objects.filter(room =room_id ,status='Booked' )
          except room.DoesNotExist:
              return Response({"message": "room {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          except bed.DoesNotExist:
              return Response({"message": "bed {room_id} dosen't exist"}, status=status.HTTP_404_NOT_FOUND)
          serializerRoom = RoomSerializer(room, many=True)
          serializerBed = BedSerializer(bed, many=True)
          return Response({"RoomData": serializerRoom.data,"BedDate":serializerBed.data}) 
    

class UpdateRoom(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def patch(self, req, bed_id):
        try:    
            bed =   Bed.objects.get(id =bed_id )
            room =   Room.objects.get( id=bed.room.pk )
        except room.DoesNotExist:
            return Response({"message": "Room does not exist"},  status=status.HTTP_404_NOT_FOUND)
        except bed.DoesNotExist:
            return Response({"message": "Bed does not exist"},  status=status.HTTP_404_NOT_FOUND)
        
        serializer = updateRoomSerializer(data=req.data)
        if serializer.is_valid():
            patients=User.objects.get(id=serializer.data.get('patients'))
            incharge=User.objects.get(employee=serializer.data.get('incharge'))
            doctors=User.objects.get(employee=serializer.data.get('doctors'))
            nurses=User.objects.get(employee=serializer.data.get('nurses'))
            
            room.number_in_room = serializer.data.get('number_in_room',  room.number_in_room)
            room.status = serializer.data.get('room_status',  room.status)
            room.incharge=incharge

           
            bed.patients=patients
            bed.doctors=doctors
            bed.nurses=nurses
            bed.status  = serializer.data.get('bed_status', bed.status)
            bed.disease= serializer.data.get('disease', bed.disease)
            bed.treatment= serializer.data.get('treatment', bed.treatment)
            bed.descrption= serializer.data.get('descrption', bed.descrption)
            bed.reserved_from= serializer.data.get('reserved_from', bed.reserved_from)
            bed.reserved_until= serializer.data.get('reserved_until', bed.reserved_until)
            room.save()
            bed.save()
            return Response({"message": "Room data updated successfully", "Room" : RoomSerializer(room).data,"Bed":BedSerializer(bed).data})
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)



class AddRoom(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def post(self, req, bed_id):
        try:    
            bed =   Bed.objects.get(id =bed_id )
            Oldroom =   Room.objects.get( id=bed.room.pk )
        except Oldroom.DoesNotExist:
            return Response({"message": "Room does not exist"},  status=status.HTTP_404_NOT_FOUND)
        except bed.DoesNotExist:
            return Response({"message": "Bed does not exist"},  status=status.HTTP_404_NOT_FOUND)
        
        serializer = updateRoomSerializer(data=req.data)
        if serializer.is_valid():

            patients=User.objects.get(id=serializer.data.get('patients'))
            incharge=User.objects.get(employee=serializer.data.get('incharge'))
            doctors=User.objects.get(employee=serializer.data.get('doctors'))
            nurses=User.objects.get(employee=serializer.data.get('nurses'))
  
            Oldroom.number_in_room = serializer.data.get('number_in_room',  Oldroom.number_in_room)
            Oldroom.status = serializer.data.get('room_status',  Oldroom.status)
            Oldroom.incharge=incharge

            NewBed=Bed(
                name=bed.name,
                room=bed.room,


                patients=patients,
                doctors=doctors,
                nurses=nurses,
                
                status  = serializer.data.get('bed_status', bed.status),
                disease= serializer.data.get('disease', bed.disease),
                treatment= serializer.data.get('treatment', bed.treatment),
                descrption= serializer.data.get('descrption', bed.descrption),
                reserved_from= serializer.data.get('reserved_from', bed.reserved_from),
                reserved_until= serializer.data.get('reserved_until', bed.reserved_until),
            )
            Oldroom.save()
            NewBed.save()
            return Response({"message": "Room data updated successfully", "Room" : RoomSerializer(Oldroom).data,"Bed":BedSerializer(bed).data})
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)







########################################Calls


class GetAllCalls(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req):
          try:
              Call =   Calls.objects.all()
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 


class GetCalls(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req,Call_id):
          try:
              Nurse = req.user
              Call =   Calls.objects.filter(nurse = Nurse,id=Call_id)
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 
    

class GetCurrentCalls(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req):
          try:
              Nurse = req.user
              Call =   Calls.objects.filter(nurse = Nurse, status='Pending' )
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 
    

class GetCallsHistory(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req):
          try:
              Nurse = req.user
              Call =   Calls.objects.filter(nurse = Nurse, status='Done' )
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 
    

    
class CreateCalls(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def post(self, req):
          
          serializer = CreateCallSerializer(data=req.data)
          
          if serializer.is_valid():
                
                patients=User.objects.get(id=serializer.data.get('patients'))
                
                doctors=User.objects.get(employee=serializer.data.get('doctors'))
                nurses=User.objects.get(employee=serializer.data.get('nurses'))
                room=Room.objects.get(id=serializer.data.get('room'))
                bed=Bed.objects.get(id=serializer.data.get('bed'))
                call=Calls(
                    
                    patients=patients,
                    doctors=doctors,
                    nurses=nurses,

                    bed=bed,
                    room=room,

                    type= serializer.data.get('type'),
                    status  = serializer.data.get('status'),
                    disease= serializer.data.get('disease'),
                    treatment= serializer.data.get('treatment'),
                    descrption= serializer.data.get('descrption'),
                    date= serializer.data.get('date'),
                )

                call.save()
                return Response({"message": "Room data updated successfully", "Call" : CallsSerializer(call).data})
          return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)


class UpdateCall(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def patch(self, req, Call_id):
        try:    
            call =   Calls.objects.get(id =Call_id )
        except call.DoesNotExist:
            return Response({"message": "cal does not exist"},  status=status.HTTP_404_NOT_FOUND)
        
        serializer = CreateCallSerializer(data=req.data)
        if serializer.is_valid():
            patients=User.objects.get(id=serializer.data.get('patients'))
            doctors=User.objects.get(employee=serializer.data.get('doctors'))
            nurses=User.objects.get(employee=serializer.data.get('nurses'))
            room=Room.objects.get(id=serializer.data.get('room'))
            bed=Bed.objects.get(id=serializer.data.get('bed'))

            call.bed=bed,
            call.room=room,

            call.patients=patients
            call.doctors=doctors
            call.nurses=nurses

            call.type = serializer.data.get('type',  call.type)
            call.status  = serializer.data.get('status', call.status)
            call.disease= serializer.data.get('disease', call.disease)
            call.treatment= serializer.data.get('treatment', call.treatment)
            call.descrption= serializer.data.get('descrption', call.descrption)
            call.date= serializer.data.get('date', call.date)

            call.save()
            return Response({"message": "Call data updated successfully", "data" : CallsSerializer(call).data})
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)

