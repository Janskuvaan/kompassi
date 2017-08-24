# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-24 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yukicon2018', '0002_auto_20170824_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupextra',
            name='total_work',
            field=models.CharField(choices=[('10h', 'Minimi - 10 tuntia'), ('12h', '10-12 tuntia'), ('yli12h', 'Työn Sankari! Yli 12 tuntia!')], help_text='Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana?', max_length=15, verbose_name='Toivottu kokonaistyömäärä'),
        ),
    ]
