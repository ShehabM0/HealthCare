from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from patients.models import *
from doctors.models import *
from .serializers import *
from .permissions import IsNurse
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime

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
              working_hour = WorkingHour.objects.filter(clinic_id=Nurse.employee.clinic, day__gte=datetime.now()).first()              
              PatientsReserv =   Reservation.objects.filter(clinic = Nurse.employee.clinic, working_hour=working_hour, status='A')
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
    



class NurseChatDetails(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNurse]

    def get(self, req):


        users = User.objects.all()
        res=[]
        for user in users :
            if not user.employee is None:
                res.append(user)

        serializer = ChatSerializer(res, many=True)


        return Response(serializer.data)





################################## Room 



class GetAllRooms(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req):
        
        bed = Bed.objects.all()
        serializer = BedSerializer(bed, many=True)
        return Response({"data": serializer.data, "count": len(serializer.data)}) 


class GetCurrentRoom(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNurse]

    def get(self, req,room_id):
          try:
              room =   Room.objects.filter(id =room_id )
              bed =   Bed.objects.filter(room =room_id ,status='Empty')| Bed.objects.filter(room =room_id ,status='Occupied')
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
            patients = Bed.objects.get(id =bed_id).patients if serializer.data.get('patients') is None else User.objects.get(id=serializer.data.get('patients'))
            incharge= Room.objects.get(id=bed.room.pk).incharge if serializer.data.get('incharge') is None else User.objects.get(employee=serializer.data.get('incharge'))
            doctors= Bed.objects.get(id =bed_id).doctors if serializer.data.get('doctors') is None else User.objects.get(employee=serializer.data.get('doctors'))
            nurses= Bed.objects.get(id =bed_id).nurses if serializer.data.get('nurses') is None else User.objects.get(employee=serializer.data.get('nurses'))


            if  serializer.data.get('number_in_room') is not None  :           
                room.number_in_room = serializer.data.get('number_in_room',  room.number_in_room)
            if  serializer.data.get('room_status') is not None  :
                room.status = serializer.data.get('room_status',  room.status)
            if  serializer.data.get('incharge') is not None  :
                room.incharge=incharge

            if  serializer.data.get('patients') is not None  :
                bed.patients=patients
            if  serializer.data.get('doctors') is not None  :               
                bed.doctors=doctors
            if  serializer.data.get('nurses') is not None  :
                bed.nurses=nurses
            if  serializer.data.get('bed_status') is not None  :
                bed.status  = serializer.data.get('bed_status', bed.status)
            if  serializer.data.get('disease') is not None  :
                bed.disease= serializer.data.get('disease', bed.disease)
            if  serializer.data.get('treatment') is not None  :
                bed.treatment= serializer.data.get('treatment', bed.treatment)
            if  serializer.data.get('descrption') is not None  :
                bed.descrption= serializer.data.get('descrption', bed.descrption)
            if  serializer.data.get('reserved_from') is not None  :
                bed.reserved_from= serializer.data.get('reserved_from', bed.reserved_from)
            if  serializer.data.get('reserved_until') is not None  :
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

            patients= None if serializer.data.get('patients') is None else User.objects.get(id=serializer.data.get('patients'))
            incharge= None if serializer.data.get('incharge') is None else User.objects.get(employee=serializer.data.get('incharge'))
            doctors= None if serializer.data.get('doctors') is None else User.objects.get(employee=serializer.data.get('doctors'))
            nurses= None if serializer.data.get('nurses') is None else User.objects.get(employee=serializer.data.get('nurses'))
  
            Oldroom.number_in_room = serializer.data.get('number_in_room')
            Oldroom.status = serializer.data.get('room_status')
            Oldroom.incharge=incharge

            NewBed=Bed(
                
                name=bed.name,
                room=bed.room,


                patients=patients,
                doctors=doctors,
                nurses=nurses,
                
                status  = serializer.data.get('bed_status'),
                disease= serializer.data.get('disease'),
                treatment= serializer.data.get('treatment'),
                descrption= serializer.data.get('descrption'),
                reserved_from= serializer.data.get('reserved_from'),
                reserved_until= serializer.data.get('reserved_until'),
            )
            Oldroom.save()
            NewBed.save()
            return Response({"message": "Room data updated successfully", "Room" : RoomSerializer(Oldroom).data,"Bed":BedSerializer(NewBed).data})
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
                
                patients= None if serializer.data.get('patients') is None else User.objects.get(id=serializer.data.get('patients'))
                
                doctors= None if serializer.data.get('doctors') is None else User.objects.get(employee=serializer.data.get('doctors'))
                nurse= None if serializer.data.get('nurse') is None else User.objects.get(employee=serializer.data.get('nurse'))
                room= None if serializer.data.get('room') is None else Room.objects.get(id=serializer.data.get('room'))
                bed= None if serializer.data.get('bed') is None else Bed.objects.get(id=serializer.data.get('bed'))
                call=Calls(


                    patients=patients,
                    doctors=doctors,
                    nurse=nurse,

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
                return Response({"message": "call data Created successfully", "Call" : CallsSerializer(call).data})
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
            patients= Calls.objects.get(id =Call_id).patients if serializer.data.get('patients') is None else User.objects.get(id=serializer.data.get('patients'))
            doctors= Calls.objects.get(id =Call_id).doctors if serializer.data.get('doctors') is None else User.objects.get(employee=serializer.data.get('doctors'))
            nurse= Calls.objects.get(id =Call_id).nurse if serializer.data.get('nurse') is None else User.objects.get(employee=serializer.data.get('nurse'))
            room= Calls.objects.get(id =Call_id).room if serializer.data.get('room') is None else   Room.objects.get(id=serializer.data.get('room'))
            bed= Calls.objects.get(id =Call_id).bed if serializer.data.get('bed') is None else Bed.objects.get(id=serializer.data.get('bed'))


            if  serializer.data.get('bed') is not None  : 
                call.bed=bed
            if  serializer.data.get('room') is not None  : 
                call.room=room

            if  serializer.data.get('patients') is not None  :                
                call.patients=patients
            if  serializer.data.get('doctors') is not None  : 
                call.doctors=doctors
            if  serializer.data.get('nurse') is not None  : 
                call.nurses=nurse
            if  serializer.data.get('type') is not None  : 
                call.type = serializer.data.get('type',  call.type)
            if  serializer.data.get('status') is not None  : 
                call.status  = serializer.data.get('status', call.status)
            if  serializer.data.get('disease') is not None  : 
                call.disease= serializer.data.get('disease', call.disease)
            if  serializer.data.get('treatment') is not None  : 
                call.treatment= serializer.data.get('treatment', call.treatment)
            if  serializer.data.get('descrption') is not None  : 
                call.descrption= serializer.data.get('descrption', call.descrption)
            if  serializer.data.get('date') is not None  : 
                call.date= serializer.data.get('date', call.date)

            call.save()
            return Response({"message": "Call data updated successfully", "data" : CallsSerializer(call).data})
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)

