from rest_framework.decorators import api_view, permission_classes
from .models import MedicationCategory, Medication, Prescription
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import status
from patients.models import User
from common.permissions import *
from .serializers import *

from payment.views import AddPurchase
from django.http import HttpRequest

@swagger_auto_schema(method='POST', request_body=AddMedicationSerializer)
@swagger_auto_schema(method='GET')
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Medications(req):
    if req.method == 'GET':
        return ListMedications(req)
    elif req.method == 'POST':
        return AddMedication(req)
    
def ListMedications(req):
    req_page_number = req.GET.get("page")
    if not req_page_number:
        return Response({"message": "Page parameter is missing!"}, status=status.HTTP_400_BAD_REQUEST)

    filter_by = req.GET.get("filterby", "")
    keyword = req.GET.get("keyword", "")
    if filter_by == 'name':
        medicines = Medication.objects.filter(name__icontains=keyword)
    elif filter_by == 'category':
        categories = MedicationCategory.objects.filter(category__icontains=keyword)
        medicines = Medication.objects.filter(category__in=categories)
    else:
        medicines = Medication.objects.all()

    paginator = Paginator(medicines, 10)
    page_number = int(req_page_number)
    page_obj = paginator.get_page(page_number)
    serializer = MedicationSerializer(page_obj, many=True)

    if page_number > paginator.num_pages:
        return Response({"data": [], "count": 0}, status=status.HTTP_404_NOT_FOUND)
    return Response({"data": serializer.data, "count": len(serializer.data)})

def AddMedication(req):
    user = req.user
    if not user.employee or user.employee.type != 'P':
        return Response({"message": "User is not a Pharmacist."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = AddMedicationSerializer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Medication not added!", "errros": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response({"message": "Medication added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='GET')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListRelatedMedications(req, medication_id):
    try:
        medicaiton = Medication.objects.get(id=medication_id)
    except Medication.DoesNotExist:
        return Response({"message": "Medication not found!"}, status=status.HTTP_404_NOT_FOUND)

    categories = medicaiton.category.all()
    medicines = Medication.objects.filter(category__in=categories)
    serializer = MedicationSerializer(medicines, many=True)

    return Response({"data": serializer.data, "count": len(serializer.data)})

@swagger_auto_schema(method='POST', request_body=PrescriptionSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def CreatePrescription(req, patient_id):
    doctor_id = req.user.id
    try:
        doctor = User.objects.get(id=doctor_id)
        if doctor.employee and doctor.employee.type != "D":
            return Response({"message": "Not authorized, User isn't a doctor!"}, status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        return Response({"message": "Doctor not found!"}, status=status.HTTP_404_NOT_FOUND)

    try:
        patient = User.objects.get(id=patient_id)
    except User.DoesNotExist:
        return Response({"message": "Patient not found!"}, status=status.HTTP_404_NOT_FOUND)

    prescription = Prescription.objects.create(doctor=doctor, patient=patient)
    serializer = PrescriptionSerializer(prescription)
    return Response({"message": "Prescription created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='POST', request_body=PrescriptionItemSerializer)
@swagger_auto_schema(method='GET')
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def PrescriptionsItems(req, prescription_id):
    if req.method == 'GET':
        return ListPrescriptionItems(req, prescription_id)
    elif req.method == 'POST':
        return AddToPrescription(req, prescription_id)

def AddToPrescription(req, prescription_id):
    try:
        prescription = Prescription.objects.get(id=prescription_id)
    except Prescription.DoesNotExist:
        return Response({"message": "Prescription not found!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PrescriptionItemSerializer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Prescription Item isn't valid!"}, status=status.HTTP_400_BAD_REQUEST)

    medication = Medication.objects.get(id=serializer.data['medication'])
    if not medication.available:
        return Response({"message": "Medicaiton isn't available!"}, status=status.HTTP_400_BAD_REQUEST)

    PrescriptionItem.objects.create(
        prescription=prescription,
        medication=medication,
        instructions=serializer.data['instructions']
    )

    return Response({"message": "Item added successfully."}, status=status.HTTP_201_CREATED)

def ListPrescriptionItems(req, prescription_id):
    try:
        prescription = Prescription.objects.get(id=prescription_id)
        prescription_items = prescription.items.all()
    except Prescription.DoesNotExist:
        return Response({"message": "Prescription not found!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ListPrescriptionItemSerializer(prescription_items, many=True)
    return Response({"data": serializer.data})

@swagger_auto_schema(method='DELETE')
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsDoctor])
def RemoveFromPrescription(req, prescription_id, prescription_item_id):
    try:
        prescription_item = PrescriptionItem.objects.get(id=prescription_item_id, prescription=prescription_id).delete()
    except PrescriptionItem.DoesNotExist:
        return Response({"message": "Prescription item not found!"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"message": "Prescription item deleted successfully."}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='DELETE')
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsDoctor])
def ClearPrescription(req, prescription_id):
    try:
        prescription = Prescription.objects.get(id=prescription_id)
        prescription.items.all().delete()
    except Prescription.DoesNotExist:
        return Response({"message": "Prescription not found!"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"message":"Prescriptions items deleted."}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='POST')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddPrescriptionPurchase(req, prescription_id):
    try:
        prescription = Prescription.objects.get(id=prescription_id)
        prescription_items = prescription.items.all()
    except Prescription.DoesNotExist:
        return Response({"message": "Prescription not found!"}, status=status.HTTP_404_NOT_FOUND)
    
    total_cost = 0
    for item in prescription_items:
        total_cost += item.medication.cost

    django_request = HttpRequest()
    django_request.method = req.method
    django_request.META = req.META
    django_request.data = {
        "payment_type": "pharmacy",
        "amount": total_cost
    }
    response = AddPurchase(django_request)
    if response.status_code == 200:
        prescription.purchased = True
        prescription.save()

    return response

@swagger_auto_schema(method='GET')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListPatientPrescriptions(req, patient_username):
    try:
        patient = User.objects.get(username=patient_username)
    except User.DoesNotExist:
        return Response({"message": "Patient not found!"}, status=status.HTTP_404_NOT_FOUND)

    patient_prescriptions = patient.prescriptions_received.all()
    serializer = ListPrescriptionSerializer(patient_prescriptions, many=True)
    return Response({"data": serializer.data})



@swagger_auto_schema(method='GET')
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPharmacist])
def VerifyPrescriptionPurchase(req, prescription_id):
    try:
        prescription = Prescription.objects.get(id=prescription_id)
    except Prescription.DoesNotExist:
        return Response({"message": "Prescription not found!"}, status=status.HTTP_404_NOT_FOUND)

    res = { 
        "message": "Prescription hasn't been purhased yet!",
        "purchased": False
    }

    if prescription.purchased:
        res["message"] = "Prescription is purhased."
        res["purchased"] = True
        prescription.purchased = False
        prescription.save()

    return Response(res, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['GET', 'DELETE'])
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated, IsPharmacist])
def MedicationCategories(req, medication_id, category_id):
    if req.method == 'GET':
        return AddMedicationCategory(req, medication_id, category_id)
    elif req.method == 'DELETE':
        return RemoveMedicationCategory(req, medication_id, category_id)

def AddMedicationCategory(req, medication_id, category_id):
    try:
        medicaiton = Medication.objects.get(id=medication_id)
    except Medication.DoesNotExist:
        return Response({"message": "Medication not found!"}, status=status.HTTP_404_NOT_FOUND)

    try:
        category = MedicationCategory.objects.get(id=category_id)
    except MedicationCategory.DoesNotExist:
        return Response({"message": "Medication Category not found!"}, status=status.HTTP_404_NOT_FOUND)

    medicaiton.category.add(category)

    categories = medicaiton.category.all()
    serializer = MedicationCategorySerilaizer(categories, many=True)

    return Response({"message": "Category added to medication successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

def RemoveMedicationCategory(req, medication_id, category_id):
    try:
        medicaiton = Medication.objects.get(id=medication_id)
    except Medication.DoesNotExist:
        return Response({"message": "Medication not found!"}, status=status.HTTP_404_NOT_FOUND)

    try:
        category = MedicationCategory.objects.get(id=category_id)
    except MedicationCategory.DoesNotExist:
        return Response({"message": "Medication Category not found!"}, status=status.HTTP_404_NOT_FOUND)
    
    category_exist = medicaiton.category.filter(id=category_id).exists()
    
    if not category_exist:
        return Response({"message": "Category doesn't belong to specified medication!"}, status=status.HTTP_404_NOT_FOUND)
    
    medicaiton.category.remove(category)

    categories = medicaiton.category.all()
    serializer = MedicationCategorySerilaizer(categories, many=True)

    return Response({"message": "Category removed from medication successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='GET')
@swagger_auto_schema(method='PATCH', request_body=AddMedicationSerializer)
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def MedicationsID(req, medication_id):
    if req.method == 'GET':
        return GetMedication(req, medication_id)
    elif req.method == 'PATCH':
        return UpdateMedication(req, medication_id)

def GetMedication(req, medication_id):
    try:
        medicaiton = Medication.objects.get(id=medication_id)
    except Medication.DoesNotExist:
        return Response({"message": "Medication not found!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MedicationSerializer(medicaiton)

    return Response({"data": serializer.data})

def UpdateMedication(req, medication_id):
    user = req.user
    if not user.employee or user.employee.type != 'P':
        return Response({"message": "User is not a Pharmacist."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        medicaiton = Medication.objects.get(id=medication_id)
    except Medication.DoesNotExist:
        return Response({"message": "Medication not found!"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AddMedicationSerializer(medicaiton, data=req.data, partial=True)
    if not serializer.is_valid():
        return Response({"message": "Medication not updated!", "errros": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    return Response({"message": "Medication updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='GET')
@swagger_auto_schema(method='POST', request_body=AddMedicationCategorySerilaizer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsPharmacist])
def Categories(req):
    if req.method == 'GET':
        return ListCategories(req)
    elif req.method == 'POST': 
        return AddCategory(req)

def ListCategories(req):
    categories = MedicationCategory.objects.all()
    serializer = MedicationCategorySerilaizer(categories, many=True)
    return Response({"data": serializer.data})

def AddCategory(req):
    serializer = AddMedicationCategorySerilaizer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Category not added!", "errros": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    return Response({"message": "Category added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
