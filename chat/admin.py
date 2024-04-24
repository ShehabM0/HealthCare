from django.contrib import admin
from .models import ChatRoom, ChatMessage

class ChatMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(ChatRoom)
admin.site.register(ChatMessage, ChatMessageAdmin)

