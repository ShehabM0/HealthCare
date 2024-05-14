from .models import CreditCard, Purchase, UserCard
from django.contrib import admin

class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(UserCard)
admin.site.register(CreditCard)
admin.site.register(Purchase, PurchaseAdmin)
