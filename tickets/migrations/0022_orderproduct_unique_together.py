# Generated by Django 1.10.7 on 2017-07-02 13:08
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0021_auto_20161211_1549"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="orderproduct",
            unique_together={("order", "product")},
        ),
    ]
