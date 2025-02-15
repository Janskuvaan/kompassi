# Generated by Django 2.1.12 on 2019-09-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nekocon2019", "0002_auto_20190421_1919"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="shirt_size",
            field=models.CharField(
                choices=[
                    ("NO_SHIRT", "Ei paitaa"),
                    ("XS", "XS Unisex"),
                    ("S", "S Unisex"),
                    ("M", "M Unisex"),
                    ("L", "L Unisex"),
                    ("XL", "XL Unisex"),
                    ("XXL", "XXL Unisex"),
                    ("3XL", "XXXL Unisex"),
                    ("LF_XS", "XS Ladyfit"),
                    ("LF_S", "S Ladyfit"),
                    ("LF_M", "M Ladyfit"),
                    ("LF_L", "L Ladyfit"),
                    ("LF_XL", "XL Ladyfit"),
                    ("LF_XXL", "XXL Ladyfit"),
                ],
                default="NO_SHIRT",
                help_text="Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan.",
                max_length=8,
                verbose_name="Paidan koko",
            ),
        ),
    ]
