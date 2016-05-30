from constance import config
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.shortcuts import get_list_or_404
from employees.models import Employee


class Command(BaseCommand):
    help = 'Update last month,current month, last year and current year scores when current date is 1st day of the month or year.'

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

    def change_day(self):
        employees = get_list_or_404(Employee)
        for employee in employees:
            employee.yesterday_given = employee.today_given
            employee.yesterday_received = employee.today_received
            employee.today_given = 0
            employee.today_received = 0
            employee.save()

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
                    subject = "User blocked in AllStars Belatrix"
                    message = "Your username %s is blocked. Please contact with your team leader to see more details." % (employee.username)
                    send_email = EmailMessage(subject, message, to=[employee.email])
                    send_email.send()
            except Exception as e:
                print e

    def send_daily_email(self):
        subject = "[Allstars] cronjob in heroku"
        message = "Confirmation mail, Heroku scheduler has been executed today."
        send_mail = EmailMessage(subject, message, to=['sergio@neosergio.net'])
        send_mail.send()


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
        parser.add_argument('--force-day',
                            action='store_true',
                            dest='force-day',
                            default=False,
                            help='Force to change current day to tomorrow')

    def handle(self, *args, **options):
        today = datetime.now()

        # Cron tasks
        if today.hour == 0:
            self.change_day()
            self.evaluate_block_users()
            self.send_daily_email()
        if today.day == 1:
            self.change_month()
        if (today.day == 1 and today.month == 1):
            self.change_year()

        # Force actions
        if options['force-day']:
            self.change_day()
            self.evaluate_block_users()
            self.send_daily_email()
        if options['force-month']:
            self.change_month()
        if options['force-year']:
            self.change_year()
