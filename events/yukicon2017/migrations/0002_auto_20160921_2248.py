# Generated by Django 1.9.9 on 2016-09-21 19:48


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("yukicon2017", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="work_days",
            field=models.ManyToManyField(
                help_text="Min\xc3\xa4 p\xc3\xa4ivin\xc3\xa4 olet halukas ty\xc3\xb6skentelem\xc3\xa4\xc3\xa4n?",
                to="yukicon2017.EventDay",
                verbose_name="Tapahtumap\xe4iv\xe4t",
            ),
        ),
    ]
