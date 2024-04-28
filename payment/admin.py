from django.contrib import admin
from .models import CreditCard, Purchase

class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(CreditCard)
admin.site.register(Purchase, PurchaseAdmin)
