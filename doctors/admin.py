from django.contrib import admin
from .models import Clinic

# Register your models here.


from .models import WorkingHour

admin.site.register(WorkingHour)
admin.site.register(Clinic)