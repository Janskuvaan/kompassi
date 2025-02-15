
from .views import survey_view, survey_export_view
from django.urls import re_path


urlpatterns = [
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/surveys/(?P<survey_slug>[a-z0-9-]+)/?$",
        survey_view,
        name="event_survey_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/surveys/(?P<survey_slug>[a-z0-9-]+)\.(?P<format>csv|tsv|xlsx)$",
        survey_export_view,
        name="event_survey_export_view",
    ),
    re_path(
        r"^surveys/(?P<survey_slug>[a-z0-9-]+)/?$",
        survey_view,
        dict(event_slug=""),
        name="global_survey_view",
    ),
    re_path(
        r"^surveys/(?P<survey_slug>[a-z0-9-]+)\.(?P<format>csv|tsv|xlsx)$",
        survey_export_view,
        dict(event_slug=""),
        name="global_survey_export_view",
    ),
]
