# Generated by Django 2.1.12 on 2019-09-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("desuprofile_integration", "0005_auto_20160124_2328"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connection",
            name="desuprofile_username",
            field=models.CharField(blank=True, max_length=150, verbose_name="Desuprofiilin käyttäjänimi"),
        ),
    ]
