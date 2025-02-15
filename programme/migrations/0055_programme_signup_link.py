# Generated by Django 1.9.9 on 2017-02-23 00:37


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programme", "0054_auto_20170212_2334"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="signup_link",
            field=models.CharField(
                blank=True,
                default="",
                help_text="If the programme requires signing up in advance, put a link here and it will be shown as a button in the schedule.",
                max_length=255,
                verbose_name="Signup link",
            ),
        ),
    ]
