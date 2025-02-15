# Generated by Django 1.9.1 on 2016-01-28 21:27


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("desucon2016", "0002_auto_20160128_2321"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="desu_amount",
            field=models.PositiveIntegerField(
                help_text="Kuinka monessa Desuconissa olet ty\xf6skennellyt?", verbose_name="Desum\xe4\xe4r\xe4"
            ),
        ),
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
                    ("3XL", "3XL Unisex"),
                    ("4XL", "4XL Unisex"),
                    ("5XL", "5XL Unisex"),
                    ("LF_XS", "XS Ladyfit"),
                    ("LF_S", "S Ladyfit"),
                    ("LF_M", "M Ladyfit"),
                    ("LF_L", "L Ladyfit"),
                    ("LF_XL", "XL Ladyfit"),
                ],
                help_text='Ajoissa ilmoittautuneet saavat maksuttoman ty\xf6voimapaidan. Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" target="_blank">ladyfit-paita</a>',
                max_length=8,
                verbose_name="Paidan koko",
            ),
        ),
    ]
