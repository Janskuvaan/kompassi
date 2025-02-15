# Generated by Django 2.1.12 on 2019-09-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programme", "0093_programme_paikkala_icon"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="is_paikkala_public",
            field=models.BooleanField(
                default=True,
                help_text="If selected, this programme will be shown in listings as publicly reservable while it is in its reservation period. Non-publicly reservable programmes can only be accessed by knowing the direct URL.",
                verbose_name="Publicly reservable",
            ),
        ),
    ]
