# Generated by Django 1.9.5 on 2016-06-09 21:05


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("badges", "0017_badgemanagementproxy"),
    ]

    operations = [
        migrations.AddField(
            model_name="badge",
            name="arrived_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Arrived at"),
        ),
    ]
