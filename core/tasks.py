import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import call_command

from celery import shared_task


logger = logging.getLogger("kompassi")


@shared_task(ignore_result=True)
def send_email(**opts):
    if settings.DEBUG:
        logger.debug(opts["body"])

    EmailMessage(**opts).send(fail_silently=False)


@shared_task(ignore_result=True)
def person_apply_state_async(person_id):
    from .models import Person

    person = Person.objects.get(id=person_id)
    person._apply_state_async()


@shared_task(ignore_result=True)
def person_apply_state_new_user_async(person_id, password):
    from .models import Person

    person = Person.objects.get(id=person_id)
    person._apply_state_new_user_async(password)


@shared_task(ignore_result=True)
def run_admin_command(*args, **kwargs):
    call_command(*args, **kwargs)
