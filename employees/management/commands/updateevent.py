from django.core.management.base import BaseCommand
from django.shortcuts import get_list_or_404
from django.utils import timezone
from events.models import Event


class Command(BaseCommand):
    help = 'Update event when current date is greater than event date'

    def evaluate_event(self):
        today = timezone.now()
        events = get_list_or_404(Event)
        for event in events:
            if today.date() <= event.datetime.date():
                event.is_upcoming = False
                event.save()

    def add_arguments(self, parser):
        parser.add_argument('--force-evaluation',
                            action='store_true',
                            dest='force-evaluation',
                            default=False,
                            help='Force to evaluate event dates')

    def handle(self, *args, **options):
        today = timezone.now()

        # Cron tasks
        if today.hour == 0:
            self.evaluate_event()

        # Force actions
        if options['force-evaluation']:
            self.evaluate_event()
