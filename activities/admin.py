from django.contrib import admin
from .models import Activity, Message


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'text', 'to_user')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'text', 'from_user', 'to_user')


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Message, MessageAdmin)
