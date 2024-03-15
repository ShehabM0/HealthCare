from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from patients.models import User

class CreateUserSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=1)
    specialization = serializers.CharField(max_length=50)

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
            raise ValidationError("First name must be at least 2 characters.")
        if len(data['last_name']) < 2:
            raise ValidationError("Last name must be at least 2 characters.")
        if len(data['phone']) < 11:
            raise ValidationError("Phone number must be at least 11 characters.")
        if data['phone'][0:2] != '01':
            raise ValidationError("Phone number must start with 01")
        if len(data['ssn']) != 14:
            raise ValidationError("Social Security number must be 14 digits.")
        if len(data['insurance_number']) != 9:
            raise ValidationError("Insurance number must be 9 digits.")
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'