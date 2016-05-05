# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-05 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0005_populate_recipient_group_job_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body_template',
            field=models.TextField(help_text='Teksti {{ signup.formatted_job_categories_accepted }} korvataan listalla hyv\xe4ksytyn v\xe4nk\xe4rin teht\xe4v\xe4alueista ja teksti {{ signup.formatted_shifts }} korvataan v\xe4nk\xe4rin vuoroilla. K\xe4ytt\xe4ess\xe4si n\xe4it\xe4 muotoilukoodeja laita ne omiksi kappaleikseen ts. reunusta ne tyhjill\xe4 riveill\xe4.', verbose_name='Viestin teksti'),
        ),
    ]
