from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import status
from .models import CreditCard
from .serilaizer import *

@swagger_auto_schema(method='POST', request_body=CreateCardSerializer)
@api_view(['POST'])
def CreateCard(req):
    user = req.user
    if not user.is_authenticated:
        return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
    if not user.is_superuser:
        return Response({"message": "User not authorized!"}, status=status.HTTP_403_FORBIDDEN)

    
    serializer = CreateCardSerializer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Invalid data!", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    card = CreditCard.objects.filter(number=serializer.data['number'])
    if card.exists():
        return Response({"message": "Card already exists!"}, status=status.HTTP_409_CONFLICT)

    card = CreditCard.objects.create(
        number=serializer.data['number'],
        expiry_month=serializer.data['expiry_month'],
        expiry_year=serializer.data['expiry_year'],
        cvv=serializer.data['cvv'],
        balance=serializer.data['balance']
    )

    return Response({"message": "success", "data": serializer.data})

@swagger_auto_schema(method='POST', request_body=AssignCardSerializer)
@api_view(['POST'])
def AssignCard(req):
    user = req.user

    serializer = AssignCardSerializer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Invalid data!", "errors": serializer.errors})

    try:
        card = CreditCard.objects.get(number=serializer.data['number'])
        card_serializer = CardSerializer(card, many=False)
    except CreditCard.DoesNotExist:
        return Response({"message": "Card doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)

    if(not matchCard(card_serializer, serializer)):
        return Response({"message": "Card data doesn't match!"}, status=status.HTTP_400_BAD_REQUEST)

    remember_card = req.GET.get('remember_card', None)
    if remember_card.lower() == 'true':
        user.remember_card = datetime.now()
    else:
        user.remember_card = None
    user.save()

    card.user = user

    return Response({"message:": "Card assigned to user successfully."})

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def NeglectCards(req):
    user = req.user

    CreditCard.objects.filter(user=user).update(user=None)

    user.remember_card = None
    user.save()

    return Response({"message": "User's card(s) have been neglected successfully."})

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def ListCards(req):
    user = req.user

    cards = CreditCard.objects.filter(user=user)
    cards = ListCardSerializer(cards, many=True)

    return Response({"data": cards.data})

@swagger_auto_schema(method='POST', request_body=AddPurchaseSerializer)
@api_view(['POST'])
def AddPurchase(req):
    user = req.user

    cards = CreditCard.objects.filter(user=user)
    if not cards.exists():
        return Response({"message": "User has no cards!"}, status=status.HTTP_402_PAYMENT_REQUIRED)
    
    serializer = AddPurchaseSerializer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Invalid data!", "errors": serializer.errors})

    cards = ListCardSerializer(cards, many=True)
    purchase_card = None
    for card in cards.data:
        card_number = card['number']
        get_card = CreditCard.objects.get(number=card_number)
        if get_card.balance > serializer.data['amount']:
            purchase_card = get_card
            get_card.balance -= serializer.data['amount']
            get_card.save()
            break

    purchase_instance = Purchase(
        payment_type=serializer.data['payment_type'],
        user=user,
        card=purchase_card,
        amount=serializer.data['amount'],
        success=True,
        created_at=datetime.now()
    )

    start_date = user.remember_card
    end_date = start_date + timedelta(days=7)
    if datetime.now() > end_date:
        CreditCard.objects.filter(user=user).update(user=None)
        user.remeber_card = None
        user.save()
    
    if purchase_card is None:
        purchase_instance.success = False
        purchase_instance.save()
        return Response({"message": "Not enough balance in your card(s)!"}, status=status.HTTP_400_BAD_REQUEST)
    purchase_instance.save()
    return Response({"message": "Purchase completed successfully"})

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def ListPurchases(req):
    user = req.user

    complete = req.GET.get('complete', '')
    if complete.lower() == "true":
        purchases = Purchase.objects.filter(user=user.id, success=True)
    elif complete.lower() == "false":
        purchases = Purchase.objects.filter(user=user.id, success=False)
    else:
        purchases = Purchase.objects.filter(user=user.id)
    purchases = ListPurchasesSerializer(purchases, many=True)

    return Response({"data": purchases.data})

def matchCard(card, serializer):
    if(
        card.data['expiry_month'] != serializer.data['expiry_month']
       ) or (
        card.data['expiry_year'] != serializer.data['expiry_year']
       ) or (
        card.data['cvv'] != serializer.data['cvv']
       ):
       return False
    return True