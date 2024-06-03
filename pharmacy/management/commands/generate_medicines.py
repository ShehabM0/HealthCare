from django.core.management.base import BaseCommand
from ..utils import GenerateMedicines 

class Command(BaseCommand):
    def handle(self, *args, **options):
        GenerateMedicines()
