from django.db import models

from labour.models import ObsoleteSignupExtraBaseV1

from core.utils import validate_slug


SHIFT_TYPE_CHOICES = [
    ("none", "Ei väliä"),
    ("4h", "Pari pitkää vuoroa"),
    ("yli4h", "Useita lyhyitä vuoroja"),
]

SHIRT_SIZES = [
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
]

SHIRT_TYPES = [
    ("STAFF", "Staff"),
    ("DESURITY", "Desurity"),
    ("KUVAAJA", "Kuvaaja"),
    ("VENDOR", "Myynti"),
    ("TOOLATE", "Myöhästyi paitatilauksesta"),
]


class SignupExtra(ObsoleteSignupExtraBaseV1):
    shift_type = models.CharField(
        max_length=15,
        verbose_name="Toivottu työvuoron pituus",
        help_text="Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?",
        choices=SHIFT_TYPE_CHOICES,
    )

    desu_amount = models.PositiveIntegerField(
        verbose_name="Desumäärä",
        help_text="Kuinka monessa Desuconissa olet ollut vänkärinä?",
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name="Työkokemus",
        help_text="Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista "
        "tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä "
        "hakemassasi tehtävässä.",
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Vapaa alue",
        help_text="Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole "
        "omaa kenttää yllä, käytä tätä kenttää."
        "Jos haet valokuvaajaksi, kerro lisäksi millaista kuvauskalustoa sinulla on käytettävissäsi ja listaa"
        "muutamia gallerialinkkejä, joista pääsemme ihailemaan ottamiasi kuvia.",
    )

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        default="NO_SHIRT",
        verbose_name="Paidan koko",
        help_text="Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan. "
        'Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" '
        'target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" '
        'target="_blank">ladyfit-paita</a>',
    )

    shirt_type = models.CharField(
        max_length=8,
        choices=SHIRT_TYPES,
        default="TOOLATE",
        verbose_name="Paidan tyyppi",
    )

    night_work = models.BooleanField(
        verbose_name="Olen valmis tekemään yötöitä",
        default=False,
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm
