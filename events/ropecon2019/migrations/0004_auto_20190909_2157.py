# Generated by Django 2.1.12 on 2019-09-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ropecon2019", "0003_auto_20190403_2159"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="certificate_delivery_address",
            field=models.TextField(
                blank=True,
                help_text="Todistukset toimitetaan ensisijaisesti sähköpostitse, mutta jos haluat todistuksesi paperilla kirjaa tähän postiosoite(katuosoite, postinumero ja toimipaikka), johon haluat todistuksen toimitettavan.",
                verbose_name="Työtodistuksen toimitusosoite",
            ),
        ),
    ]
