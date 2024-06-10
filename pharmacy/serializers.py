from rest_framework import serializers
from .models import *

class MedicationCategorySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = MedicationCategory
        fields = '__all__'

class AddMedicationCategorySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = MedicationCategory
        fields = ('category',)

class MedicationSerializer(serializers.ModelSerializer):
    category = MedicationCategorySerilaizer(many=True)

    class Meta:
        model = Medication
        fields = '__all__'

class AddMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        exclude = ('category',) 

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ['medication', 'instructions']

class ListPrescriptionSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        exclude = ('patient',) 

    def get_doctor(self, obj):
        first_name = obj.doctor.first_name
        return first_name
        
class ListPrescriptionItemSerializer(serializers.ModelSerializer):
    medication = serializers.SerializerMethodField()

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medication', 'instructions']

    def get_medication(self, obj):
        res = obj.medication.name
        return res

