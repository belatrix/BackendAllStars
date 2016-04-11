from django import forms
from django.contrib import admin
from .models import Employee, Role


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('username', 'password',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


class EmployeeAdmin(admin.ModelAdmin):
    form = UserCreationForm
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
