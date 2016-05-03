from django.contrib import admin
from .models import Star


class StarAdmin(admin.ModelAdmin):
    list_display = ('date', 'from_user', 'to_user', 'category', 'subcategory', 'keyword')

admin.site.register(Star, StarAdmin)
