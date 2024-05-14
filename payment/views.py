from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import CreditCard, UserCard
from rest_framework import status
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
    if not user.is_authenticated:
        return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = AssignCardSerializer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Invalid data!", "errors": serializer.errors})

    try:
        card = CreditCard.objects.get(number=serializer.data['number'])
        card_serializer = GetCardSerilaizer(card, many=False)
    except CreditCard.DoesNotExist:
        return Response({"message": "Card doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)

    if(not matchCard(card_serializer, serializer)):
        return Response({"message": "Card data doesn't match!"}, status=status.HTTP_400_BAD_REQUEST)

    userCard_instance = UserCard(
        user = user,
        card = card,
        remember_at = None
    )
    
    # one-to-many relationship
    try:
        exist_user_card = UserCard.objects.get(card=card);
        exist_user_card.user = user
        exist_user_card.remember_at = None
    except UserCard.DoesNotExist:
        exist_user_card = None

    remember_card = req.GET.get('remember_card', None)
    if remember_card.lower() == 'true':
        if exist_user_card: exist_user_card.remember_at = datetime.now()
        else: userCard_instance.remember_at = datetime.now()

    if exist_user_card: exist_user_card.save()
    else: userCard_instance.save()

    return Response({"message:": "Card assigned to user successfully."})

@swagger_auto_schema(method='DELETE')
@api_view(['DELETE'])
def NeglectCards(req):
    user = req.user
    if not user.is_authenticated:
        return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)

    cards = UserCard.objects.filter(user=user)
    for card in cards:
        card.delete()

    return Response({"message": "User's card(s) have been neglected successfully."})

@swagger_auto_schema(method='DELETE')
@api_view(['DELETE'])
def NeglectCard(req, pk=None):
    user = req.user
    if not user.is_authenticated:
        return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user_card = UserCard.objects.get(card=pk)
        user_card.delete()
    except UserCard.DoesNotExist:
        return Response({"message": "Card not found in user's cards list!"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"message": "User's card(s) have been neglected successfully."})

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def ListCards(req):
    user = req.user
    if not user.is_authenticated:
        return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)

    cards = UserCard.objects.filter(user=user)
    cards = UserCardSerializer(cards, many=True)

    return Response({"data": cards.data})

@swagger_auto_schema(method='POST', request_body=AddPurchaseSerializer)
@api_view(['POST'])
def AddPurchase(req):
    user = req.user
    if not user.is_authenticated:
        return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)

    cards = UserCard.objects.filter(user=user)
    if not cards.exists():
        return Response({"message": "User has no cards!"}, status=status.HTTP_402_PAYMENT_REQUIRED)
    
    serializer = AddPurchaseSerializer(data=req.data)
    if not serializer.is_valid():
        return Response({"message": "Invalid data!", "errors": serializer.errors})

    cards = ListCardSerializer(cards, many=True)
    purchase_card = None
    for card in cards.data:
        card_id = card['card']
        get_card = CreditCard.objects.get(id=card_id)
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

    for card in cards.data:
        card_id = card['card']
        get_card = UserCard.objects.get(card=card_id)
        start_date = get_card.remember_at
        if not start_date:
            get_card.delete()
        else:
            end_date = start_date + timedelta(days=7)
            if datetime.now() > end_date:
                get_card.delete()

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

    page_number = req.GET.get('page', '')
    if not page_number:
        serializer = ListPurchasesSerializer(purchases, many=True)
        return Response({"data": serializer.data, "count": len(serializer.data)})

    paginator = Paginator(purchases, 10)
    page_number = int(page_number)
    page_obj = paginator.get_page(page_number)
    serializer = ListPurchasesSerializer(page_obj, many=True)

    if page_number > paginator.num_pages:
        return Response({"data": [], "count": 0}, status=status.HTTP_404_NOT_FOUND)
    return Response({"data": serializer.data, "count": len(serializer.data)})

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