from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # list_display = ('fullname', 'subject', 'created_at', 'get_username', 'get_email')
    readonly_fields = ('created_at', 'get_username', 'get_email')

    def get_username(self, obj):
        return obj.user.username if obj.user else 'N/A'

    def get_email(self, obj):
        return obj.user.email if obj.user else 'N/A'

    get_username.short_description = 'Username'
    get_email.short_description = 'Email'

