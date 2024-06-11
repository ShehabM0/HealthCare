from django.core.management.base import BaseCommand
from ..utils import InsertMedicinesImages 

class Command(BaseCommand):
    def handle(self, *args, **options):
        InsertMedicinesImages()

