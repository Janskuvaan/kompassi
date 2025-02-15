# Generated by Django 1.10.8 on 2017-11-13 19:58
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("intra", "0005_teammember_override_job_title"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="team",
            options={"ordering": ("event", "order", "name"), "verbose_name": "Team", "verbose_name_plural": "Teams"},
        ),
        migrations.AlterField(
            model_name="teammember",
            name="override_job_title",
            field=models.CharField(
                blank=True,
                default="",
                help_text="If set, this will override the job title of this person for the purposes of this team only. If unset, the above job title field will be used. This field will not affect badge printing.",
                max_length=63,
                verbose_name="Job title in this team",
            ),
        ),
        migrations.AlterField(
            model_name="teammember",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="team_memberships",
                to="core.Person",
                verbose_name="Person",
            ),
        ),
        migrations.AlterField(
            model_name="teammember",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="members",
                to="intra.Team",
                verbose_name="Team",
            ),
        ),
    ]
