from django.contrib import admin

# Register your models here.


from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(MedicalHistory)
admin.site.register(MedicalRecord)