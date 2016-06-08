from sys import stderr

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '[event_slug...]'
    help = 'Create missing badges for programme'

    def handle(*args, **opts):
        from programme.models import Programme
        from core.models import Event
        from badges.models import Badge

        for event_slug in args[1:]:
            event = Event.objects.get(slug=event_slug)

            for programme in Programme.objects.filter(category__event=event):
                programme.apply_state()
