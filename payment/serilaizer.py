from rest_framework.exceptions import ValidationError
from .models import CreditCard, Purchase
from rest_framework import serializers
from datetime import datetime

class CreateCardSerializer(serializers.ModelSerializer):
    number = serializers.CharField(max_length=16)
    expiry_month = serializers.IntegerField()
    expiry_year = serializers.IntegerField()
    cvv = serializers.IntegerField()
    balance = serializers.IntegerField()

    class Meta:
        model = CreditCard
        fields = '__all__'

    def validate(self, data):
        if len(data['number']) != 16:
            raise ValidationError({"number": "Card number must be 16 digit!"})

        try: 
            expiry_month = int(data['expiry_month'])
            if not 0 < expiry_month < 13:
                raise ValidationError({"expiry_month": "Card expiry month must be a digit between 1 and 12!"})
        except:
            raise ValidationError({"expiry_month": "Card expiry month must be a digit between 1 and 12!"})
        try: 
            expiry_year = int(data['expiry_year'])
            if len(str(data['expiry_year'])) != 4 or expiry_year < 0:
                raise ValidationError({"expiry_year": "Card expiry year must be a positive 4-digit!"})
        except:
            raise ValidationError({"expiry_year": "Card expiry year must be a positive 4-digit!"})
        try:
            cvv = int(data['cvv'])
        except:
            raise ValidationError({"cvv": "Card cvv must be a 3-digit!"})
        try:
            balance = int(data['balance'])
            if balance < 0:
                raise ValidationError({"balance": "Card balance must be a positve integer!"})
        except:
            raise ValidationError({"balance": "Card balance must be a positve integer!"})

        return data


class AssignCardSerializer(serializers.ModelSerializer):
    number = serializers.CharField(max_length=16)
    expiry_month = serializers.IntegerField()
    expiry_year = serializers.IntegerField()
    cvv = serializers.IntegerField()

    class Meta:
        model = CreditCard
        exclude = ['balance']

    def validate(self, data):
        current_date = datetime.now()
        if len(data['number']) != 16:
            raise ValidationError({"number": "Card number must be 16 digit!!"})

        try: 
            expiry_month = int(data['expiry_month'])
            if not 0 < expiry_month < 13:
                raise ValidationError({"expiry_month": "Card expiry month must be a digit between 1 and 12!!"})
        except:
            raise ValidationError({"expiry_month": "Card expiry month must be a digit between 1 and 12!!"})
        try: 
            expiry_year = int(data['expiry_year'])
            if len(str(data['expiry_year'])) != 4 or expiry_year < 0:
                raise ValidationError({"expiry_year": "Card expiry year must be a positive 4-digit!!"})
        except:
            raise ValidationError({"expiry_year": "Card expiry year must be a postive 4-digit!!"})
        try:
            cvv = int(data['cvv'])
        except:
            raise ValidationError({"cvv": "Card cvv must be a digit!!"})


        if (expiry_year < current_date.year
            ) or (
                expiry_year == current_date.year and expiry_month < current_date.month):
            raise ValidationError({"error": "Card is expired!!"})

        return data
    
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = '__all__'

class ListCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['id', 'number']



class AddPurchaseSerializer(serializers.ModelSerializer):
    payment_type = serializers.CharField(max_length=32)
    amount = serializers.IntegerField()

    class Meta:
        model = Purchase
        fields = ['payment_type', 'amount']
    
    def validate(self, data):
        if data['payment_type'] not in ['reservation', 'pharmacy']:
            raise ValidationError({"payment_type": "Payment type must be reservation either pharmacy!"})
        
        try:
            amount = int(data['amount'])
            if amount < 0:
                raise ValidationError({"amount": "amount must be positive number"})
        except:
            raise ValidationError({"amount": "amount must be positive number"})

        return data

class ListPurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

