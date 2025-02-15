# Generated by Django 1.9.4 on 2016-04-06 16:21


from django.db import migrations, models
import django.db.models.deletion
import labour.models.signup_extras


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_auto_20160202_2235"),
        ("desucon2016", "0005_auto_20160306_1125"),
    ]

    operations = [
        migrations.CreateModel(
            name="SignupExtraV2",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "shift_type",
                    models.CharField(
                        choices=[
                            ("none", "Ei v\xe4li\xe4"),
                            ("4h", "Pari pitk\xe4\xe4 vuoroa"),
                            ("yli4h", "Useita lyhyit\xe4 vuoroja"),
                        ],
                        help_text="Haluatko tehd\xe4 yhden pitk\xe4n ty\xf6vuoron vaiko monta lyhyemp\xe4\xe4 vuoroa?",
                        max_length=15,
                        verbose_name="Toivottu ty\xf6vuoron pituus",
                    ),
                ),
                (
                    "desu_amount",
                    models.PositiveIntegerField(
                        help_text="Kuinka monessa Desuconissa olet ty\xf6skennellyt?", verbose_name="Desum\xe4\xe4r\xe4"
                    ),
                ),
                (
                    "prior_experience",
                    models.TextField(
                        blank=True,
                        help_text="Kerro t\xe4ss\xe4 kent\xe4ss\xe4, jos sinulla on aiempaa kokemusta vastaavista teht\xe4vist\xe4 tai muuta sellaista ty\xf6kokemusta, josta arvioit olevan hy\xf6ty\xe4 hakemassasi teht\xe4v\xe4ss\xe4.",
                        verbose_name="Ty\xf6kokemus",
                    ),
                ),
                (
                    "free_text",
                    models.TextField(
                        blank=True,
                        help_text="Jos haluat sanoa hakemuksesi k\xe4sittelij\xf6ille jotain sellaista, jolle ei ole omaa kentt\xe4\xe4 yll\xe4, k\xe4yt\xe4 t\xe4t\xe4 kentt\xe4\xe4. Jos haet valokuvaajaksi, kerro lis\xe4ksi millaista kuvauskalustoa sinulla on k\xe4ytett\xe4viss\xe4si ja listaamuutamia gallerialinkkej\xe4, joista p\xe4\xe4semme ihailemaan ottamiasi kuvia. ",
                        verbose_name="Vapaa alue",
                    ),
                ),
                (
                    "special_diet_other",
                    models.TextField(
                        blank=True,
                        help_text="Jos noudatat erikoisruokavaliota, jota ei ole yll\xe4 olevassa listassa, ilmoita se t\xe4ss\xe4. Tapahtuman j\xe4rjest\xe4j\xe4 pyrkii ottamaan erikoisruokavaliot huomioon, mutta kaikkia erikoisruokavalioita ei v\xe4ltt\xe4m\xe4tt\xe4 pystyt\xe4 j\xe4rjest\xe4m\xe4\xe4n.",
                        verbose_name="Muu erikoisruokavalio",
                    ),
                ),
                (
                    "shirt_size",
                    models.CharField(
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
                (
                    "shirt_type",
                    models.CharField(
                        choices=[
                            ("STAFF", "Staff"),
                            ("DESURITY", "Desurity"),
                            ("KUVAAJA", "Kuvaaja"),
                            ("VENDOR", "Myynti"),
                            ("TOOLATE", "My\xf6h\xe4styi paitatilauksesta"),
                        ],
                        default="STAFF",
                        max_length=8,
                        verbose_name="Paidan tyyppi",
                    ),
                ),
                (
                    "night_work",
                    models.BooleanField(default=False, verbose_name="Olen valmis tekem\xe4\xe4n y\xf6t\xf6it\xe4"),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="desucon2016_signup_extras",
                        to="core.Event",
                    ),
                ),
                (
                    "person",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="desucon2016_signup_extra",
                        to="core.Person",
                    ),
                ),
                (
                    "special_diet",
                    models.ManyToManyField(blank=True, to="desucon2016.SpecialDiet", verbose_name="Erikoisruokavalio"),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(labour.models.signup_extras.SignupExtraMixin, models.Model),
        ),
    ]
