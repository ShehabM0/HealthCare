from datetime import datetime, timedelta
from ..models import CreditCard
from random import randrange
from faker import Faker

faker = Faker()

def GenerateCards(num_of_cards):

    for _ in range(num_of_cards):
        num = faker.unique.credit_card_number(card_type="mastercard")
        date = faker.credit_card_expire(start=datetime.now(), end=datetime.now()+timedelta(days=5*365)).split('/')
        cvv = faker.credit_card_security_code(card_type="mastercard")
        balance=randrange(10, 10**5)

        CreditCard.objects.create(
            number=num,
            expiry_month=date[0],
            expiry_year=date[1],
            cvv=cvv,
            balance=balance
        )


