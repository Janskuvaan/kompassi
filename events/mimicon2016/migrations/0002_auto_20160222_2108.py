# Generated by Django 1.9.1 on 2016-02-22 19:08


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mimicon2016", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="want_certificate",
            field=models.BooleanField(
                default=False, verbose_name="Haluan todistuksen ty\xf6skentelyst\xe4ni Mimiconissa"
            ),
        ),
    ]
