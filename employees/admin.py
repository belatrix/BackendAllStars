from .models import Employee, Location, Role
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password using "
                                                    "<a href=\'../password/\'>this form</a>."))

    class Meta:
        model = Employee
        fields = ('email',)

    def clean_password(self):
        return self.initial['password']


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


class EmployeeAdmin(BaseUserAdmin):
    form = UserChangeForm
    list_display = ("username", "first_name", "last_name", "email", 'location', 'level', 'total_score',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'reset_password_code')}),
        ('Personal info', {'fields': ('first_name',
                                      'last_name',
                                      'role',
                                      'location',
                                      'skype_id',
                                      'avatar',
                                      'categories')}),
        ('Personal score', {'fields': ('last_month_score',
                                       'last_year_score',
                                       'current_month_score',
                                       'current_year_score',
                                       'level',
                                       'total_score')}),
        ('Permissions', {'fields': ('groups',
                                    'user_permissions',
                                    'is_superuser',
                                    'is_staff',
                                    'is_active',)}),
        ('History', {'fields': ('date_joined', 'last_login')})
    )

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Role, RoleAdmin)
