from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "budget", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("name", "email", "company", "budget", "message", "created_at")
