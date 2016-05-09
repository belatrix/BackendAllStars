from datetime import datetime
from django.core.management.base import BaseCommand
from django.shortcuts import get_list_or_404
from employees.models import Employee


class Command(BaseCommand):
    help = 'Update last month,current month, last year and current year scores when current date is 1st day of the month or year.'

    def change_month(self):
        employees = get_list_or_404(Employee)
        for employee in employees:
            employee.last_month_score = employee.current_month_score
            employee.current_month_score = 0
            employee.save()

    def change_year(self):
        employees =get_list_or_404(Employee)
        for employee in employees:
            employee.last_year_score = employee.current_year_score
            employee.current_year_score = 0
            employee.save()

    def add_arguments(self, parser):
        parser.add_argument('--force-month',
                            action='store_true',
                            dest='force-month',
                            default=False,
                            help='Force to change current month score to last month score')
        parser.add_argument('--force-year',
                            action='store_true',
                            dest='force-year',
                            default=False,
                            help='Force to change current year score to last year score')

    def handle(self, *args, **options):
        today = datetime.now()
        if today.day == 1:
            self.change_month()
        if (today.day == 1 and today.month == 1):
            self.change_year()
        if  options['force-month']:
            self.change_month()
        if options['force-year']:
            self.change_year()
