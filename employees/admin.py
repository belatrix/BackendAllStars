from django.contrib import admin
from .models import Employee, Role


class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", 'level', 'score',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name',
                                      'last_name',
                                      'role',
                                      'skype_id',
                                      'avatar',
                                      'categories')}),
        ('Personal score', {'fields': ('last_month_score',
                                       'current_month_score',
                                       'level',
                                       'score')}),
        ('Permissions', {'fields': ('groups',
                                    'user_permissions',
                                    'is_superuser',
                                    'is_staff',
                                    'is_active',)}),
        ('History', {'fields': ('date_joined', 'last_login')})
    )

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Role, RoleAdmin)
