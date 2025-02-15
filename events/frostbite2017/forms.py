from django import forms
from django.db.models import Q

from crispy_forms.layout import Layout, Fieldset

from core.utils import horizontal_form_helper, indented_without_label
from labour.forms import AlternativeFormMixin, SignupForm
from labour.models import Signup, JobCategory
from programme.models import AlternativeProgrammeFormMixin
from programme.forms import ProgrammeSelfServiceForm

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "shift_type",
            indented_without_label("night_work"),
            Fieldset(
                "Lisätiedot",
                # 'shirt_size',
                "special_diet",
                "special_diet_other",
                "desu_amount",
                "prior_experience",
                "free_text",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "shift_type",
            # 'shirt_size',
            "special_diet",
            "special_diet_other",
            "desu_amount",
            "night_work",
            "prior_experience",
            "free_text",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )


class OrganizerSignupForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        admin = kwargs.pop("admin")

        assert not admin

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Tehtävän tiedot",
                "job_title",
            ),
        )

        self.fields["job_title"].help_text = "Mikä on tehtäväsi vastaavana? Printataan badgeen."
        # self.fields['job_title'].required = True

    class Meta:
        model = Signup
        fields = ("job_title",)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
            special_diet=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(job_categories=JobCategory.objects.filter(event__slug="frostbite2017", name="Vastaava"))


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Lisätiedot",
                # 'shirt_size',
                "special_diet",
                "special_diet_other",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            # 'shirt_size',
            "special_diet",
            "special_diet_other",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            shift_type="none",
            desu_amount=666,
            free_text="Syötetty käyttäen vastaavan ilmoittautumislomaketta",
        )


class ProgrammeSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            # 'shirt_size',
            "special_diet",
            "special_diet_other",
        )

    class Meta:
        model = SignupExtra
        fields = (
            # 'shirt_size',
            "special_diet",
            "special_diet_other",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            shift_type="none",
            desu_amount=666,
            free_text="Syötetty käyttäen ohjelmanjärjestäjän ilmoittautumislomaketta",
        )


class SpecialistSignupForm(SignupForm, AlternativeFormMixin):
    def get_job_categories_query(self, event, admin=False):
        assert not admin

        return Q(event__slug="frostbite2017", public=False) & ~Q(slug="vastaava")

    def get_excluded_field_defaults(self):
        return dict(
            notes="Syötetty käyttäen jälki-ilmoittautumislomaketta",
        )


class SpecialistSignupExtraForm(SignupExtraForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "shift_type",
            indented_without_label("night_work"),
            Fieldset(
                "Lisätiedot",
                # 'shirt_size',
                "special_diet",
                "special_diet_other",
                "desu_amount",
                "prior_experience",
                "free_text",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "shift_type",
            # 'shirt_size',
            "special_diet",
            "special_diet_other",
            "desu_amount",
            "night_work",
            "prior_experience",
            "free_text",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )


class ProgrammeForm(ProgrammeSelfServiceForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].disabled = True
        self.fields["title"].help_text = None
        self.fields["title"].required = False
        self.fields["description"].disabled = True
        self.fields[
            "description"
        ].help_text = "Et voi muuttaa ohjelman otsikkoa tai kuvausta tässä, sillä ne päivittyvät Kompassiin suoraan Desusaitin ohjelmakartasta. Jos otsikkoa tai kuvausta on tarpeen muuttaa, ota yhteyttä ohjelmavastaavaan."
        self.fields["description"].required = False
