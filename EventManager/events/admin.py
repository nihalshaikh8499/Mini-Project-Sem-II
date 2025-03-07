from django.contrib import admin
from .models import Event, EventRegistration

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date', 'time', 'venue')

class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'phone_number', 'department')  # Add fields to display
    list_filter = ('event', 'department')
    search_fields = ('phone_number',)

admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)