from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ('updated_at',)

admin.site.register(Employee, EmployeeAdmin)
