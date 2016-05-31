from constance import config
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.shortcuts import get_list_or_404
from employees.models import Employee


class Command(BaseCommand):
    help = "Update scores daily."

    def change_day(self):
        employees = get_list_or_404(Employee)
        for employee in employees:
            employee.yesterday_given = employee.today_given
            employee.yesterday_received = employee.today_received
            employee.today_given = 0
            employee.today_received = 0
            employee.save()

    def change_month(self):
        employees = get_list_or_404(Employee)
        for employee in employees:
            employee.last_month_given = employee.current_month_given
            employee.last_month_score = employee.current_month_score
            employee.current_month_given = 0
            employee.current_month_score = 0
            employee.save()

    def change_year(self):
        employees = get_list_or_404(Employee)
        for employee in employees:
            employee.last_year_given = employee.current_year_given
            employee.last_year_score = employee.current_year_score
            employee.current_year_given = 0
            employee.current_year_score = 0
            employee.save()

    def send_daily_email(self):
        subject = config.DAILY_EXECUTION_CONFIRMATION_SUBJECT
        message = config.DAILY_EXECUTION_CONFIRMATION_MESSAGE
        email = EmailMessage(subject, message, to=[config.DAILY_EXECUTION_CONFIRMATION_EMAIL])
        email.send()

    def send_blocked_notification_email(self, employee):
        subject = config.USER_BLOCKED_NOTIFICATION_SUBJECT
        message = config.USER_BLOCKED_NOTIFICATION_MESSAGE % employee.username
        email = EmailMessage(subject, message, to=[employee.email])
        email.send()

    def evaluate_block_users(self):
        employees = get_list_or_404(Employee)
        for employee in employees:
            if employee.yesterday_given > config.MAX_STARS_GIVEN_DAY:
                employee.is_blocked = True
            if employee.yesterday_received > config.MAX_STARS_RECEIVED_DAY:
                employee.is_blocked = True
            if employee.current_month_given > config.MAX_STARS_GIVEN_MONTHLY:
                employee.is_blocked = True
            if employee.current_month_score > config.MAX_STARS_RECEIVED_MONTHLY:
                employee.is_blocked = True
            employee.save()

            try:
                if employee.is_blocked:
                    self.send_blocked_notification_email()
            except Exception as e:
                print e

    def handle(self, *args, **options):
        today = datetime.now()
        self.change_day()
        self.evaluate_block_users()
        self.send_daily_email()

        if today.day == 1:
            self.change_month()
        if (today.day == 1 and today.month == 1):
            self.change_year()
