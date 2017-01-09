from .models import Event, EventActivity, EventParticipant
from django.contrib import admin


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'is_upcoming')


class EventActivityAdmin(admin.ModelAdmin):
    list_display = ('event', 'datetime', 'text')


class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'participant', 'datetime')


admin.site.register(Event, EventAdmin)
admin.site.register(EventActivity, EventActivityAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
