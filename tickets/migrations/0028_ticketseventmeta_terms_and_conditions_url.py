# Generated by Django 2.2.24 on 2022-04-18 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0027_auto_20220316_2255"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticketseventmeta",
            name="terms_and_conditions_url",
            field=models.CharField(
                blank=True,
                default="",
                help_text="If set, customers will be required to indicate acceptance to finish order.",
                max_length=1023,
                verbose_name="Terms and conditions URL",
            ),
        ),
    ]
