from django.contrib import admin
from .models import *

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date', 'time', 'venue')


class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'phone_number', 'department', 'first_player_name', 'first_player_roll_number')

    def first_player_name(self, obj):
        if obj.players and isinstance(obj.players, list) and len(obj.players) > 0:
            return obj.players[0].get("name", "N/A")
        return "N/A"

    def first_player_roll_number(self, obj):
        if obj.players and isinstance(obj.players, list) and len(obj.players) > 0:
            return obj.players[0].get("roll_number", "N/A")
        return "N/A"

    first_player_name.short_description = "Name"
    first_player_roll_number.short_description = "Roll No."
    list_filter = ('event', 'department')
    search_fields = ('phone_number',)


class AllowedEmailAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)


class VolunteerRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'phone_number', 'department', 'name', 'rollnumber')
    list_filter = ('event', 'department')
    search_fields = ('phone_number', 'name')


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 5


@admin.register(EventHighlight)
class EventHighlightAdmin(admin.ModelAdmin):
    inlines = [EventImageInline]
    list_display = ('title', 'created_at')


admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)
admin.site.register(AllowedEmail, AllowedEmailAdmin)
admin.site.register(ContactFormModel)
admin.site.register(VolunteerRegistration, VolunteerRegistrationAdmin)