from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("labour", "0011_job_slug"),
    ]

    operations = [
        migrations.CreateModel(
            name="SignupExtra",
            fields=[
                (
                    "signup",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        related_name="+",
                        primary_key=True,
                        serialize=False,
                        to="labour.Signup",
                    ),
                ),
                (
                    "shift_type",
                    models.CharField(
                        help_text="Haluatko tehd\xe4 yhden pitk\xe4n ty\xf6vuoron vaiko monta lyhyemp\xe4\xe4 vuoroa?",
                        max_length=15,
                        verbose_name="Toivottu ty\xf6vuoron pituus",
                        choices=[
                            ("2h", "2 tunnin vuoroja"),
                            ("4h", "4 tunnin vuoroja"),
                            ("yli4h", "Yli 4 tunnin vuoroja"),
                        ],
                    ),
                ),
                (
                    "total_work",
                    models.CharField(
                        help_text="Kuinka paljon haluat tehd\xe4 t\xf6it\xe4 yhteens\xe4 tapahtuman aikana? Useimmissa teht\xe4vist\xe4 minimi on kahdeksan tuntia, mutta joissain teht\xe4viss\xe4 se voi olla my\xf6s v\xe4hemm\xe4n (esim. majoitusvalvonta 6 h).",
                        max_length=15,
                        verbose_name="Toivottu kokonaisty\xf6m\xe4\xe4r\xe4",
                        choices=[("8h", "8 tuntia"), ("yli8h", "Yli 8 tuntia")],
                    ),
                ),
                (
                    "special_diet_other",
                    models.TextField(
                        help_text="Jos noudatat erikoisruokavaliota, jota ei ole yll\xe4 olevassa listassa, ilmoita se t\xe4ss\xe4. Tapahtuman j\xe4rjest\xe4j\xe4 pyrkii ottamaan erikoisruokavaliot huomioon, mutta kaikkia erikoisruokavalioita ei v\xe4ltt\xe4m\xe4tt\xe4 pystyt\xe4 j\xe4rjest\xe4m\xe4\xe4n.",
                        verbose_name="Muu erikoisruokavalio",
                        blank=True,
                    ),
                ),
                (
                    "prior_experience",
                    models.TextField(
                        help_text="Kerro t\xe4ss\xe4 kent\xe4ss\xe4, jos sinulla on aiempaa kokemusta vastaavista teht\xe4vist\xe4 tai muuta sellaista ty\xf6kokemusta, josta arvioit olevan hy\xf6ty\xe4 hakemassasi teht\xe4v\xe4ss\xe4.",
                        verbose_name="Ty\xf6kokemus",
                        blank=True,
                    ),
                ),
                (
                    "free_text",
                    models.TextField(
                        help_text="Jos haluat sanoa hakemuksesi k\xe4sittelij\xf6ille jotain sellaista, jolle ei ole omaa kentt\xe4\xe4 yll\xe4, k\xe4yt\xe4 t\xe4t\xe4 kentt\xe4\xe4.",
                        verbose_name="Vapaa alue",
                        blank=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="SpecialDiet",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=63)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="signupextra",
            name="special_diet",
            field=models.ManyToManyField(to="kuplii2016.SpecialDiet", verbose_name="Erikoisruokavalio", blank=True),
            preserve_default=True,
        ),
    ]
