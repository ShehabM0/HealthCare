from django.contrib import admin
from .models import Bed
from .models import Room
from .models import Calls

# Register your models here.

admin.site.register(Bed)
admin.site.register(Room)
admin.site.register(Calls)
