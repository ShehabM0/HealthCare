from django.core.management.base import BaseCommand
from ..utils import GenerateCards 

class Command(BaseCommand):
    def handle(self, *args, **options):
        GenerateCards(10)

