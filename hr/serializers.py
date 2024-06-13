from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from patients.models import User
from .models import Employee

class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()

    date_of_birth = serializers.DateField()
    phone = serializers.CharField(max_length=15)
    address = serializers.CharField(max_length=100)
    ssn = serializers.CharField(min_length=14)
    insurance_number = serializers.CharField(min_length=9)

    gender = serializers.CharField(max_length=1)
    status = serializers.CharField(max_length=1)
    blood = serializers.CharField(min_length=1, max_length=3)

    def validate(self, data):
        if len(data['first_name']) < 2:
            raise ValidationError({"first_name": "First name must be at least 2 characters!"})
        if len(data['last_name']) < 2:
            raise ValidationError({"last_name": "Last name must be at least 2 characters!"})
        
        if data['phone'][0:2] != '01' or len(data['phone']) < 11 or not data['phone'].isdigit():
            raise ValidationError({"phone": "Phone number must start with 01 with at least 11 characters!"})
        if len(data['ssn']) != 14 or not data['ssn'].isdigit():
            raise ValidationError({"ssn": "Social Security number must be 14 digits!"})
        if len(data['insurance_number']) != 9 or not data['insurance_number'].isdigit():
            raise ValidationError({"insurance_number": "Insurance number must be 9 digits!"})

        return data
    
class CreateEmployeeSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=1)
    specialization = serializers.CharField(max_length=50)
    salary = serializers.IntegerField()

    def validate(self, data):
        if data['salary'] < 0:
            raise ValidationError({"salary": "Salary must be a postive digit!"})

        return data

class UpdateEmployeeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=1)
    specialization = serializers.CharField(max_length=50)
    salary = serializers.IntegerField()

    class Meta:
        model = Employee
        fields = '__all__'

    def validate_salary(self, salary):
        if salary < 0:
            raise ValidationError({"salary": "Salary must be a postive digit!"})
        return salary
    def validate_type(self, type):
        if type not in Employee.USER_TYPES_DICT.keys():
            raise ValidationError({"type": "Employee type must be (D)octor, (N)urse, (H)uman resources, (P)harmacist, (H)ead (D)octor or (H)ead (N)urse."})
        return type
    def validate_specialization(self, specialization):
        if (specialization, specialization) not in Employee.SPECIALIZAION_TYPES:
            raise ValidationError({"type": "Invalid Employee specialization!"})
        return specialization

class EmployeeSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'

    def get_type(self, obj):
        type_full_str = Employee.USER_TYPES_DICT[obj.type]
        return type_full_str
        