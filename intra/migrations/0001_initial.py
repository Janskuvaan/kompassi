# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-19 20:31
from __future__ import unicode_literals

import core.models.group_management_mixin
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0023_auto_20160704_2155'),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntraEventMeta',
            fields=[
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='intraeventmeta', serialize=False, to='core.Event')),
                ('admin_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('organizer_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_organizer_group_for_intra_event_meta', to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, core.models.group_management_mixin.GroupManagementMixin),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', help_text='What is the team responsible for?', verbose_name='Description')),
                ('slug', models.CharField(help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.', max_length=255, validators=[django.core.validators.RegexValidator(message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.', regex='[a-z0-9-]+')], verbose_name='Tekninen nimi')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Event')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'ordering': ('event', 'order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_primary_team', models.BooleanField(default=True, help_text='In some listings where space is tight, the person is only shown under their default team. Designating one team as the default for someone replaces their prior default team.', verbose_name='Default team')),
                ('is_team_leader', models.BooleanField(default=False, help_text='Team leaders are placed first and hilighted in listings.', verbose_name='Team leader')),
                ('is_shown_internally', models.BooleanField(default=True, help_text='Controls whether this person is shown in internal listings. You might want to un-tick this for people who have been added to this team for only the access or mailing lists.', verbose_name='Display internally')),
                ('is_shown_publicly', models.BooleanField(default=True, help_text='Controls whether this person is shown in public listings.', verbose_name='Display publicly')),
                ('is_group_member', models.BooleanField(default=True, help_text='Controls whether this person is added to the user group of this team. Group membership in turn usually controls membership on mailing lists and may convey additional access privileges.', verbose_name='Group membership')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='core.Person')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='intra.Team')),
            ],
            options={
                'ordering': ('team', '-is_team_leader', 'person__surname', 'person__first_name'),
                'verbose_name': 'Team member',
                'verbose_name_plural': 'Team members',
            },
        ),
        migrations.AlterUniqueTogether(
            name='teammember',
            unique_together=set([('team', 'person')]),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('event', 'slug')]),
        ),
    ]
