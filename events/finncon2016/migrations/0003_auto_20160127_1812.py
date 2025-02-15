# Generated by Django 1.9.1 on 2016-01-27 16:12


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finncon2016", "0002_auto_20160127_1806"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="shirt_size",
            field=models.CharField(
                blank=True,
                choices=[
                    ("NO_SHIRT", "Ei paitaa"),
                    ("XS", "XS Unisex"),
                    ("S", "S Unisex"),
                    ("M", "M Unisex"),
                    ("L", "L Unisex"),
                    ("XL", "XL Unisex"),
                    ("XXL", "XXL Unisex"),
                    ("3XL", "3XL Unisex"),
                    ("4XL", "4XL Unisex"),
                    ("5XL", "5XL Unisex"),
                    ("LF_XS", "XS Ladyfit"),
                    ("LF_S", "S Ladyfit"),
                    ("LF_M", "M Ladyfit"),
                    ("LF_L", "L Ladyfit"),
                    ("LF_XL", "XL Ladyfit"),
                ],
                help_text='Ajoissa ilmoittautuneet v\xe4nk\xe4rit saavat mahdollisesti maksuttoman ty\xf6voimapaidan. Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" target="_blank">ladyfit-paita</a>',
                max_length=8,
                null=True,
                verbose_name="Paidan koko",
            ),
        ),
    ]
