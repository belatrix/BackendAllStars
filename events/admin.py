from .models import Event, Participant, Talk
from django.contrib import admin


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'datetime', 'location')


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'email')


class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'datetime', 'speaker', 'location')

admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Talk, TalkAdmin)
