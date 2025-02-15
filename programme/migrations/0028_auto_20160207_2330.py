# Generated by Django 1.9.1 on 2016-02-07 21:30


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programme", "0027_auto_20160204_1842"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programme",
            name="computer",
            field=models.CharField(
                choices=[
                    ("con", "Laptop provided by the event"),
                    ("pc", "Own laptop \u2013 PC"),
                    ("mac", "Own laptop \u2013\xa0Mac"),
                    ("none", "No computer required"),
                ],
                default="con",
                help_text="What kind of a computer do you wish to use? The use of your own computer is only possible if agreed in advance.",
                max_length=4,
                verbose_name="Computer use",
            ),
        ),
        migrations.AlterField(
            model_name="programme",
            name="number_of_microphones",
            field=models.IntegerField(
                choices=[
                    (0, "0"),
                    (1, "1"),
                    (2, "2"),
                    (3, "3"),
                    (4, "4"),
                    (5, "5"),
                    (
                        99,
                        'More than five \u2013\xa0Please elaborate on your needs in the "Other tech requirements" field.',
                    ),
                ],
                default=1,
                help_text="How many microphones do you require?",
                verbose_name="Microphones",
            ),
        ),
        migrations.AlterField(
            model_name="programme",
            name="room_requirements",
            field=models.TextField(
                blank=True,
                help_text="How large an audience do you expect for your programme? What kind of a room do you wish for your programme?",
                verbose_name="Room requirements",
            ),
        ),
        migrations.AlterField(
            model_name="programme",
            name="tech_requirements",
            field=models.TextField(
                blank=True,
                help_text="Do you have tech requirements that are not covered by the previous questions?",
                verbose_name="Other tech requirements",
            ),
        ),
        migrations.AlterField(
            model_name="programme",
            name="use_audio",
            field=models.CharField(
                choices=[("yes", "Yes"), ("no", "No"), ("notsure", "Not sure")],
                default="no",
                help_text="Will you play audio in your programme?",
                max_length=7,
                verbose_name="Audio playback",
            ),
        ),
        migrations.AlterField(
            model_name="programme",
            name="use_video",
            field=models.CharField(
                choices=[("yes", "Yes"), ("no", "No"), ("notsure", "Not sure")],
                default="no",
                help_text="Will you play video in your programme?",
                max_length=7,
                verbose_name="Video playback",
            ),
        ),
    ]
