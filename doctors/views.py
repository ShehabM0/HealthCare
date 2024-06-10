from datetime import datetime
from django.shortcuts import render
from rest_framework import generics,status, permissions
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from .permissions import IsDoctor
from common.utils import get_status_word
from hr.models import Employee
from nurses.models import *

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


    

    # if clinic doesn't have a doctor will throw error 500
class ListAllClinics(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    def get(self, request):
        clinics = Clinic.objects.all()
        response = []
        for clinic in clinics:
            try:
                clinic_doctor = Employee.objects.filter(clinic=clinic, type='D').get()
                clinic_doctor_user_obj = User.objects.filter(employee=clinic_doctor.id).first()
                serializer = ClinicSerializer(clinic).data
                serializer['doctor'] = DoctorSerializer(clinic_doctor_user_obj).data
                response.append(serializer)
            except Employee.DoesNotExist:
                return Response({"message": "Clinic does not have a doctor please refer to database and fix the data error"}, status=500)
        return Response(response)
    
class GetClinicWorkingHours(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    def get(self,request, clinic_id):
        working_hours = WorkingHour.objects.filter(clinic_id=clinic_id, day__gte=datetime.now())
        serializer = WorkingHourSerializer(working_hours, many=True)
        return Response(serializer.data)

class UpdateClinicStatus(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
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
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get(self, request):
        user = request.user
        working_hour = WorkingHour.objects.filter(clinic_id=user.employee.clinic, day__gte=datetime.now()).first()
        cases = Reservation.objects.filter(clinic = user.employee.clinic, working_hour=working_hour)
        serializer = CaseSerializer(cases, many=True)
        return Response({"data": serializer.data , "count": cases.count()})
    

class UserDetails(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.status = get_status_word(user.status, User.STATUS_TYPES)
            user.gender = get_status_word(user.gender, User.STATUS_TYPES)
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=404)
        serializer = PatientSerializer(user)
        return Response(serializer.data)
    
    
class PatientMedicalRecordView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    
    def get(self, request, patient_id):
        user = User.objects.filter(id=patient_id).first()
        medicalRecords = MedicalRecord.objects.filter(patient=user)
        for file in medicalRecords:
            file.type = get_status_word(file.type, MedicalRecord.FILE_TYPES)
        serializer = MedicalRecordSerializer(medicalRecords, many=True)
        return Response({"data" : serializer.data, "count": medicalRecords.count()})
    


    
################################## Room 



class GetAllRooms(APIView):
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

    def get(self, req):
        
        room = Room.objects.all()
        serializer = RoomSerializer(room, many=True)
        return Response({"data": serializer.data, "count": len(serializer.data)}) 


class GetCurrentRoom(APIView):
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

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
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

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
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

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
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

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
            incharge=User.objects.get(Employee=serializer.data.get('incharge'))
            doctors=User.objects.get(Employee=serializer.data.get('doctors'))
            nurses=User.objects.get(Employee=serializer.data.get('nurses'))
            
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
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

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
            incharge=User.objects.get(Employee=serializer.data.get('incharge'))
            doctors=User.objects.get(Employee=serializer.data.get('doctors'))
            nurses=User.objects.get(Employee=serializer.data.get('nurses'))
  
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
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

    def get(self, req):
          try:
              Call =   Calls.objects.all()
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 


class GetCalls(APIView):
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

    def get(self, req,Call_id):
          try:
              Nurse = req.user
              Call =   Calls.objects.filter(nurse = Nurse,id=Call_id)
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 
    

class GetCurrentCalls(APIView):
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

    def get(self, req):
          try:
              Nurse = req.user
              Call =   Calls.objects.filter(nurse = Nurse, status='Pending' )
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 
    

class GetCallsHistory(APIView):
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

    def get(self, req):
          try:
              Nurse = req.user
              Call =   Calls.objects.filter(nurse = Nurse, status='Done' )
          except Call.DoesNotExist:
              return Response({"message": "there is no Calls right now"}, status=status.HTTP_404_NOT_FOUND)
          serializer = CallsSerializer(Call, many=True)
          return Response({"data": serializer.data, "count": len(serializer.data)}) 
    

    
class CreateCalls(APIView):
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

    def post(self, req):
          
          serializer = CreateCallSerializer(data=req.data)
          
          if serializer.is_valid():
                call=Calls(
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
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

    def patch(self, req, Call_id):
        try:    
            call =   Calls.objects.get(id =Call_id )
        except call.DoesNotExist:
            return Response({"message": "cal does not exist"},  status=status.HTTP_404_NOT_FOUND)
        
        serializer = CreateCallSerializer(data=req.data)
        if serializer.is_valid():

            call.type = serializer.data.get('type',  call.type)
            call.status  = serializer.data.get('status', call.status)
            call.disease= serializer.data.get('disease', call.disease)
            call.treatment= serializer.data.get('treatment', call.treatment)
            call.descrption= serializer.data.get('descrption', call.descrption)
            call.date= serializer.data.get('date', call.date)

            call.save()
            return Response({"message": "Call data updated successfully", "data" : CallsSerializer(call).data})
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)

