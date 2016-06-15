from django.contrib import admin
from .models import Activity, Message


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'detail', 'from_user', 'to_user')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'message', 'from_user', 'to_user')


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Message, MessageAdmin)
