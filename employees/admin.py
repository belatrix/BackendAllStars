from .models import Employee, Position, Location, Role, EmployeeDevice
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from import_export.admin import ImportExportMixin


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password using "
                                                    "<a href=\'../password/\'>this form</a>."))

    class Meta(object):
        model = Employee
        fields = ('email',)

    def clean_password(self):
        return self.initial['password']


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')


class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "weight")


class EmployeeAdmin(ImportExportMixin, BaseUserAdmin):
    form = UserChangeForm
    list_display = ("username", "first_name", "last_name", "email", 'location', 'level', 'total_score', 'is_blocked')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'reset_password_code', 'is_password_reset_required')}),
        ('Personal info', {'fields': ('first_name',
                                      'last_name',
                                      'location',
                                      'skype_id',
                                      'avatar',
                                      'is_base_profile_complete')}),
        ('Professional information', {'fields': ('position',
                                                 'role')}),
        ('Personal score daily', {'fields': ('today_given',
                                             'today_received',
                                             'yesterday_given',
                                             'yesterday_received')}),
        ('Personal score monthly', {'fields': ('current_month_given',
                                               'current_month_score',
                                               'last_month_given',
                                               'last_month_score')}),
        ('Personal score yearly', {'fields': ('current_year_given',
                                              'current_year_score',
                                              'last_year_given',
                                              'last_year_score')}),
        ('Personal score total', {'fields': ('total_given',
                                             'total_score',
                                             'level')}),
        ('Permissions', {'fields': ('groups',
                                    'user_permissions',
                                    'is_blocked',
                                    'is_superuser',
                                    'is_staff',
                                    'is_active',)}),
        ('History', {'fields': ('date_joined', 'last_login')})
    )


class EmployeeDeviceAdmin(admin.ModelAdmin):
    list_display = ('username', 'android_device', 'ios_device')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(EmployeeDevice, EmployeeDeviceAdmin)
