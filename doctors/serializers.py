from .models import *
from patients.models import *
from nurses.models import *
from rest_framework.exceptions import ValidationError

from rest_framework import serializers

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AddWorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = '__all__'

class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = '__all__'



class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class updateClinicStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=1, required=False)
    price = serializers.FloatField(required=False)

    def validate(self, data):
        if 'status' not in data and 'price' not in data:
            raise serializers.ValidationError({"message": "At least one of 'price' or 'status' must be provided"})
        
        if 'status' in data and data['status'] not in ['A', 'C']:
            raise serializers.ValidationError({"status": "Status should be (A)vailable or (C)losed"})
        
        if 'price' in data and data['price'] is not None and data['price'] < 0:
            raise serializers.ValidationError({"price": "Invalid price"})
        
        return data
    

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'blood', 'gender', 'status']


class CaseSerializer(serializers.ModelSerializer):
    patient = DoctorSerializer()
    class Meta:
        model = Reservation
        fields = ['id', 'status', 'type', 'patient']
        depth=1


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        exclude = ['patient']

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id','name']

class EmployeeSerializer(serializers.ModelSerializer):
    clinic=ClinicSerializer()
    class Meta:
        model = Employee
        fields = ['id', 'type','clinic'] 

class ChatSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name','employee']  



class PreserveClinicSerializer2(serializers.Serializer):
    clinic_id = serializers.IntegerField()
    working_hour_id = serializers.IntegerField()
    patient=serializers.IntegerField( required=False)
    type=serializers.CharField(max_length=2, required=False)
    def validate(self,data):
        if data['type'] not in ['S', 'C', 'V','E']:
            raise ValidationError("Invalid status. Must be (S)urgery, or (C)onsultation or (V)isit or (E)xamination .")        
        if not User.objects.filter(id=data['patient']).exists():
            raise ValidationError({"patient": "patient does not exist"})       
        if not Clinic.objects.filter(id=data['clinic_id']).exists():
            raise ValidationError({"clinic_id": "Clinic does not exist"})
        if not WorkingHour.objects.filter(id=data['working_hour_id']).exists():
            raise ValidationError({"working_hour_id": "Working hour does not exist"})
        return data

   ############################# Room

class RoomSerializer(serializers.ModelSerializer):
    incharge = DoctorSerializer()
    class Meta:
        model = Room
        fields ='__all__'
        depth = 1        



class GetRoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, required=False)
    def validate(self, data):
        if 'name' not in data :
            raise serializers.ValidationError({"message": "'name' must be provided"})
        return data
    

class BedSerializer(serializers.ModelSerializer):
    patients = DoctorSerializer()
    doctors = DoctorSerializer()
    nurses = DoctorSerializer()
    class Meta:
        model = Bed
        fields ='__all__'
        depth = 1  



class updateRoomSerializer(serializers.Serializer):
    number_in_room = serializers.IntegerField( required=False)
    room_status = serializers.CharField(max_length=13,required=False)
    incharge= serializers.IntegerField( required=False)
    bed_status  =serializers.CharField(max_length=13, required=False)
    disease=serializers.CharField(max_length=13, required=False)
    treatment=serializers.CharField(max_length=13, required=False)
    descrption=serializers.CharField(max_length=13, required=False)
    patients= serializers.IntegerField( required=False)
    doctors= serializers.IntegerField( required=False)
    nurses= serializers.IntegerField( required=False)
    reserved_from=serializers.DateTimeField(required=False)
    reserved_until=serializers.DateTimeField(required=False)

    def validate(self, data):
        # if 'room_status' not in data and 'number_in_room' not in data and 'incharge' not in data and 'bed_status' not in data and 'reserved_until' not in data and 'reserved_from' not in data and 'doctands' not in data and 'nurses' not in data and 'patients' not in data and 'disease' not in data and 'treatment' not in data and 'descrption' not in data:
        #     raise serializers.ValidationError({"message": "At least one of 'number_in_room' or 'room_status' or 'incharge' or 'bed_status' or 'reserved_from' or 'reserved_until' or 'doctors' or 'nurses' or 'patients' or 'disease' or 'treatment' or 'descrption' must be provided"})
        
        if 'room_status' in data and data['room_status'] not in ['Occupied', 'Full','Book','Empty']:
            raise serializers.ValidationError({"room_status": "Invalid status"})
        
        if 'bed_status' in data and data['bed_status'] not in ['Occupied', 'CheckOut','Booked','Empty']:
            raise serializers.ValidationError({"room_status": "Invalid status"})
        
        if 'number_in_room' in data and data['number_in_room'] is not None and data['number_in_room'] > 3:
            raise serializers.ValidationError({"number_in_room": "Invalid number_in_room max number id{max}"})
        
        if 'treatment' in data and len(data['treatment']) > 13:
            raise serializers.ValidationError({"treatment": "Invalid treatment be at least 8 characters."}) 
        
        if 'disease' in data and len(data['disease']) > 13:
            raise serializers.ValidationError({"disease": "Invalid diseasemust be at least 8 characters."})      
          
        if 'descrption' in data and len(data['descrption']) > 100:
            raise serializers.ValidationError({"descrption": "Invalid descrption be at least 100 characters."})           


        if 'incharge' in data and not Employee.objects.filter(id=data['incharge']).exists():
            raise ValidationError({"incharge": "doctor does not exist"})
      
        if 'patients' in data and not User.objects.filter(id=data['patients']).exists():
            raise ValidationError({"patients": "patient does not exist"})
        
        if 'doctors' in data and not Employee.objects.filter(id=data['doctors']).exists():
            raise ValidationError({"doctors": "doctor does not exist"})
        
        if 'nurses' in data and not Employee.objects.filter(id=data['nurses']).exists():
            raise ValidationError({"nurses": "nurse does not exist"})
        return data


###################################  Calls




class CallsSerializer(serializers.ModelSerializer):
    patients = DoctorSerializer()
    doctors = DoctorSerializer()
    nurse = DoctorSerializer()
    class Meta:
        model = Calls
        fields ='__all__'
        depth = 1   





class CreateCallSerializer(serializers.Serializer):
    type =serializers.CharField(max_length=20, required=False)
    room = serializers.IntegerField( required=False)
    disease =serializers.CharField(max_length=30, required=False)
    treatment =serializers.CharField(max_length=30, required=False)
    status =serializers.CharField(max_length=7, required=False)
    descrption =serializers.CharField(max_length=100, required=False)
    patients= serializers.IntegerField( required=False)
    doctors= serializers.IntegerField( required=False)
    nurse= serializers.IntegerField( required=False)
    date = serializers.DateTimeField(required=False)
    bed= serializers.IntegerField( required=False)

    def validate(self,data):
        if 'room' in data and  not Room.objects.filter(id=data['room']).exists():
            raise ValidationError({"room": "room does not exist"})
        
        if 'bed' in data and not Bed.objects.filter(id=data['bed']).exists():
            raise ValidationError({"bed": "bed does not exist"})        
        
        if 'patients' in data and not User.objects.filter(id=data['patients']).exists():
            raise ValidationError({"patients": "patient does not exist"})
        
        if 'doctors' in data and not Employee.objects.filter(id=data['doctors']).exists():
            raise ValidationError({"doctors": "doctor does not exist"})
        
        if 'nurse' in data and not Employee.objects.filter(id=data['nurse']).exists():
            raise ValidationError({"nurse": "nurse does not exist"})
        

        if 'status' in data and data['status'] not in ['Pending', 'Done']:
            raise ValidationError("Invalid status. Must be Pending, or Done.")
        
        if  'type' in data and data['type'] not in ['Surgery', 'inPatient Treatment']:
            raise ValidationError("Invalid type. Must be Surgery, or inPatient Treatment.")
        
        if 'disease' in data and len(data['disease']) > 30:
            raise ValidationError({"disease": "disease name must be at least 30 characters."})
        
        if 'treatment' in data and len(data['treatment']) >30:
            raise ValidationError({"treatment": "treatment name must be at least 30 characters."})
       
        if 'descrption' in data and len(data['descrption']) > 100:
            raise ValidationError({"descrption": "descrption must be at least 100 characters."})                
        return data



class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    file_name = serializers.CharField(max_length=100, required=False)
    type = serializers.CharField(max_length=1, required=False)

    def validate(self, data):
        type = data.get('type')
        if type not in ['P', 'R', 'I', 'A']:
            raise ValidationError("Invalid type. Must be (P)rescription, or (R)eport, or (I)mage, or (A)nalysis.")
        return data