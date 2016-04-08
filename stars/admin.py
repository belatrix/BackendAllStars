from django.contrib import admin
from .models import Star


class StarAdmin(admin.ModelAdmin):
    list_display = ('date', 'text')

admin.site.register(Star, StarAdmin)