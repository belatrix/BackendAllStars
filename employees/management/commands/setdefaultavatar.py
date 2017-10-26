from django.core.files import File
from django.core.management.base import BaseCommand
from django.shortcuts import get_list_or_404
from employees.models import Employee


class Command(BaseCommand):
    help = 'Set default avatar image for all employees, suggested use on development environments'

    def get_employee_list(self):
        default_image = File(open('sample_data/default_avatar.png', 'rb'))
        employees = get_list_or_404(Employee)

        for employee in employees:
            employee.avatar.save('default.png', default_image)

    def handle(self, *args, **options):
        self.get_employee_list()
