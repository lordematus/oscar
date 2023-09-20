from django.contrib import admin

from messaging.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestamp', 'sender', 'recipient', 'content']
