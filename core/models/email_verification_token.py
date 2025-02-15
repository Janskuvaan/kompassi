from django.conf import settings
from django.db import models
from django.template.loader import render_to_string

from ..utils import url
from .one_time_code import OneTimeCode


class EmailVerificationError(RuntimeError):
    pass


class EmailVerificationToken(OneTimeCode):
    email = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.person and not self.email:
            self.email = self.person.email

        return super().save(*args, **kwargs)

    def render_message_subject(self, request):
        return f"{settings.KOMPASSI_INSTALLATION_NAME}: Vahvista sähköpostiosoitteesi!"

    def render_message_body(self, request):
        vars = dict(link=request.build_absolute_uri(url("core_email_verification_view", self.code)))

        return render_to_string("core_email_verification_message.eml", vars, request=request)
