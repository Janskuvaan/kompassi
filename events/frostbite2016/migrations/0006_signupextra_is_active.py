# Generated by Django 1.9.4 on 2016-04-06 18:51


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("frostbite2016", "0005_auto_20160306_1125"),
    ]

    operations = [
        migrations.AddField(
            model_name="signupextra",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
