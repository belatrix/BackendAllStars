from .models import Comment, Event, Participant, Talk
from django.contrib import admin


class CommentAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'author', 'message', 'is_approved', 'approved_by', 'event', 'talk')


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'datetime', 'location')


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email')


class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'datetime', 'speaker', 'location')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Talk, TalkAdmin)
