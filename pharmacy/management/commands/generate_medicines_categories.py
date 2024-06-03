from django.core.management.base import BaseCommand
from ..utils import GenerateMedCategories 

class Command(BaseCommand):
    def handle(self, *args, **options):
        GenerateMedCategories()
