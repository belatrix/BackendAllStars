from django.contrib import admin
from .models import Badge, EmployeeBadge, Star


class StarAdmin(admin.ModelAdmin):
    list_display = ('date', 'from_user', 'to_user', 'category', 'keyword')


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')


class EmployeeBadgeAdmin(admin.ModelAdmin):
    list_display = ('date', 'to_user', 'assigned_by')


admin.site.register(Badge, BadgeAdmin)
admin.site.register(EmployeeBadge, EmployeeBadgeAdmin)
admin.site.register(Star, StarAdmin)
