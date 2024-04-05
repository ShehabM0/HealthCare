from rest_framework import serializers
from patients.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    address = serializers.CharField(max_length=100)
    gender = serializers.CharField(max_length=1)
    status = serializers.CharField(max_length=1)
    blood = serializers.CharField(max_length=3)
    type = serializers.CharField(max_length=1)
    date_of_birth = serializers.DateField()

    insurance_number = serializers.CharField(max_length=9)
    ssn = serializers.CharField(max_length=14)

    class Meta:
        model = User
        files = '__all__'
        exclude = ['email', 'password', 'username']

    def validate_ssn(self, value):
        user_id = self.context['user_id']
        exist_ssn = User.objects.exclude(pk=user_id).filter(ssn=value).exists()
        if exist_ssn:
            raise serializers.ValidationError({"ssn": "This ssn is already in use."})
        if len(value) != 14:
            raise serializers.ValidationError({"ssn": "ssn should be of length 14."})
        return value

    def validate_insurance_number(self, value):
        user_id = self.context['user_id']
        exist_insurance_number = User.objects.exclude(pk=user_id).filter(insurance_number=value).exists()
        if exist_insurance_number:
            raise serializers.ValidationError({"insurance_number": "This insurance number is already in use."})
        if len(value) != 9:
            raise serializers.ValidationError({"insurance_number": "Insurance number should be of length 9."})
        return value


class UpdateEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']

    def validate_email(self, email):
        user_id = self.context['user_id']
        exist_email = User.objects.exclude(pk=user_id).filter(email=email).exists()
        if exist_email:
            raise serializers.ValidationError({"email": "This email is already in use."})
        return email
    
class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
    confirm_password = serializers.CharField(max_length=30)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password and Confirm Password does not match")
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        return data

# Forgot password email verification
class VerifyEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']

    def validate_email(self, email):
        user_id = self.context['user_id']
        verify_email = User.objects.filter(id=user_id, email=email).exists()
        if not verify_email:
            raise serializers.ValidationError({"email": "Error verifying Email, make sure you entered your email correct!"})
        return email
    
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30)
    confirm_password = serializers.CharField(max_length=30)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password and Confirm Password does not match"})
        if len(data['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters."})
        return data