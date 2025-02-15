# Generated by Django 1.9.1 on 2016-01-24 12:47


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_remove_event_headline"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailverificationtoken",
            name="state",
            field=models.CharField(
                choices=[("valid", "Valid"), ("used", "Used"), ("revoked", "Revoked")], default="valid", max_length=8
            ),
        ),
        migrations.AlterField(
            model_name="passwordresettoken",
            name="state",
            field=models.CharField(
                choices=[("valid", "Valid"), ("used", "Used"), ("revoked", "Revoked")], default="valid", max_length=8
            ),
        ),
    ]
