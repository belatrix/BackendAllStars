from datetime import datetime
from django.core.management.base import BaseCommand
from django.shortcuts import get_list_or_404
from employees.models import Employee


class Command(BaseCommand):
    help = 'Update last and current month score when current date is 1st day of the month'

    def handle(self, *args, **options):
        today = datetime.now()
        if today.day == 1:
            employees = get_list_or_404(Employee)
            for employee in employees:
                employee.last_month_score = employee.current_month_score
                employee.current_month_score = 0
                employee.save()
