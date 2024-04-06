from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import VerificationCode

class CreateCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model=VerificationCode
        fields=['email']

class ValidateCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    class Meta:
        model=VerificationCode
        fields=['email', 'code']

    def validate_code(self, code):
        if len(code) != 6:
            raise ValidationError("Verification code must be 6-digits.")
        for char in code:
            if char < '0' or char > '9':
                raise ValidationError("Verification code must be 6-digits.")

class GetCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=VerificationCode
        fields='__all__'
