# Generated by Django 2.1.12 on 2019-09-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hitpoint2019", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="total_work",
            field=models.CharField(
                choices=[
                    ("6h", "Minimi – 6 tuntia"),
                    ("8h", "8 tuntia"),
                    ("12h", "10–12 tuntia"),
                    ("yli12h", "Työn Sankari! Yli 12 tuntia!"),
                ],
                help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Minimi on 6 tuntia.",
                max_length=15,
                verbose_name="Toivottu kokonaistyömäärä",
            ),
        ),
    ]
