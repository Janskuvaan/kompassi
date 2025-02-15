from unittest import TestCase as NonDatabaseTestCase

from django.test import TestCase

from core.models.event import Event
from core.models import Person
from labour.models import LabourEventMeta

from .utils import emailify
from .email_aliases import firstname_surname
from .models import Claims, CBACEntry, EmailAlias, GroupEmailAliasGrant, EmailAliasType


class FakePerson:
    first_name = "Santtu"
    surname = "Pajukanta"


class EmailifyTestCase(NonDatabaseTestCase):
    def test_emailify(self):
        self.assertEqual(emailify(""), "")
        self.assertEqual(emailify("Santtu Pajukanta"), "santtu.pajukanta")
        self.assertEqual(emailify("Kalle-Jooseppi Mäki-Kangas-Ketelä"), "kalle-jooseppi.maki-kangas-ketela")

    def test_firstname_surname(self):
        self.assertEqual(firstname_surname(FakePerson()), "santtu.pajukanta")


class EmailAliasesTestCase(TestCase):
    def setUp(self):
        self.meta, unused = LabourEventMeta.get_or_create_dummy()
        self.group = self.meta.get_group("admins")
        self.person, unused = Person.get_or_create_dummy()

    def test_email_alias_create(self):
        email_alias, unused = EmailAlias.get_or_create_dummy()
        self.assertEqual(email_alias.email_address, "markku.mahtinen@example.com")

    def test_ensure_aliases(self):
        alias_type, unused = EmailAliasType.get_or_create_dummy()

        self.group_grant, unused = GroupEmailAliasGrant.objects.get_or_create(group=self.group, type=alias_type)
        GroupEmailAliasGrant.ensure_aliases(person=self.person)

        self.assertEqual(alias_type.email_aliases.count(), 0)

        self.person.user.groups.add(self.group)
        GroupEmailAliasGrant.ensure_aliases(person=self.person)

        self.assertEqual(alias_type.email_aliases.count(), 1)

    def test_account_name_generator_returning_none(self):
        alias_type, unused = EmailAliasType.get_or_create_dummy(
            metavar="nick",
            defaults=dict(
                account_name_code="access.email_aliases:nick",
            ),
        )

        self.person.nick = ""
        self.person.save()

        self.assertEqual(alias_type.email_aliases.count(), 0)

        GroupEmailAliasGrant.ensure_aliases(self.person)

        self.assertEqual(alias_type.email_aliases.count(), 0)


def get_claims(event: Event, app_name: str) -> Claims:
    return {
        "organization": event.organization.slug,
        "event": event.slug,
        "app": app_name,
        "view": "start_view",
        "method": "POST",
    }


def test_ensure_admin_group_privileges(db):
    """
    Given there is an event that uses the labour module
    And there is a person
    When that person is given labour admin privileges for the event
    Then they can perform labour admin actions in that event
    But they cannot perform programme admin actions in that event

    When that person is stripped of labour admin privileges for the event
    Then they cannot perform labour admin actions in that event
    And they cannot perform programme admin actions in that event
    """

    meta, unused = LabourEventMeta.get_or_create_dummy()
    event = meta.event
    person, unused = Person.get_or_create_dummy()

    meta.admin_group.user_set.add(person.user)
    CBACEntry.ensure_admin_group_privileges()

    assert CBACEntry.is_allowed(person.user, get_claims(event, "labour"))
    assert not CBACEntry.is_allowed(person.user, get_claims(event, "programme"))

    meta.admin_group.user_set.remove(person.user)
    CBACEntry.ensure_admin_group_privileges()

    assert not CBACEntry.is_allowed(person.user, get_claims(event, "labour"))
    assert not CBACEntry.is_allowed(person.user, get_claims(event, "programme"))
