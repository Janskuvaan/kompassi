from django.conf import settings

from .views import (
    tickets_accommodation_view,
    tickets_address_view,
    tickets_admin_accommodation_create_view,
    tickets_admin_accommodation_presence_view,
    tickets_admin_accommodation_view,
    tickets_admin_batch_view,
    tickets_admin_batches_view,
    tickets_admin_etickets_view,
    tickets_admin_export_view,
    tickets_admin_order_view,
    tickets_admin_orders_view,
    tickets_admin_pos_view,
    tickets_admin_reports_view,
    tickets_admin_shirts_view,
    tickets_admin_stats_by_date_view,
    tickets_admin_stats_view,
    tickets_admin_tools_view,
    tickets_confirm_view,
    tickets_shirts_view,
    tickets_thanks_view,
    tickets_tickets_view,
    tickets_welcome_view,
)
from django.urls import re_path

urlpatterns = [
    re_path(r"events/(?P<event_slug>[a-z0-9-]+)/tickets/?$", tickets_welcome_view, name="tickets_welcome_view"),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/products/?$", tickets_tickets_view, name="tickets_tickets_view"
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/accommodation/?$",
        tickets_accommodation_view,
        name="tickets_accommodation_view",
    ),
    re_path(r"events/(?P<event_slug>[a-z0-9-]+)/tickets/shirts/?$", tickets_shirts_view, name="tickets_shirts_view"),
    re_path(r"events/(?P<event_slug>[a-z0-9-]+)/tickets/address/?$", tickets_address_view, name="tickets_address_view"),
    re_path(r"events/(?P<event_slug>[a-z0-9-]+)/tickets/confirm/?$", tickets_confirm_view, name="tickets_confirm_view"),
    re_path(r"events/(?P<event_slug>[a-z0-9-]+)/tickets/thanks/?$", tickets_thanks_view, name="tickets_thanks_view"),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin$", tickets_admin_stats_view, name="tickets_admin_stats_view"
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/by-date/raw$",
        tickets_admin_stats_by_date_view,
        {"raw": True},
        name="tickets_admin_stats_by_date_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/orders$",
        tickets_admin_orders_view,
        name="tickets_admin_orders_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/orders\.(?P<format>xlsx|csv)$",
        tickets_admin_export_view,
        name="tickets_admin_export_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/orders/(?P<order_id>\d+)/$",
        tickets_admin_order_view,
        name="tickets_admin_order_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/orders/(?P<order_id>\d+)/etickets.pdf$",
        tickets_admin_etickets_view,
        name="tickets_admin_etickets_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/batches$",
        tickets_admin_batches_view,
        name="tickets_admin_batches_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/batches/(?P<batch_id>\d+)$",
        tickets_admin_batch_view,
        name="tickets_admin_batch_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/accommodation/?$",
        tickets_admin_accommodation_view,
        name="tickets_admin_accommodation_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/accommodation/(?P<limit_group_id>\d+)/?$",
        tickets_admin_accommodation_view,
        name="tickets_admin_accommodation_filtered_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/accommodation/(?P<limit_group_id>\d+)/(?P<accommodation_information_id>\d+)/?$",
        tickets_admin_accommodation_presence_view,
        name="tickets_admin_accommodation_presence_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/accommodation/(?P<limit_group_id>\d+)/new/?$",
        tickets_admin_accommodation_create_view,
        name="tickets_admin_accommodation_create_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/shirts/?$",
        tickets_admin_shirts_view,
        name="tickets_admin_shirts_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/shirts\.(?P<format>csv|tsv|xlsx)$",
        tickets_admin_shirts_view,
        name="tickets_admin_shirts_export_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/tools$",
        tickets_admin_tools_view,
        name="tickets_admin_tools_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/reports/?$",
        tickets_admin_reports_view,
        name="tickets_admin_reports_view",
    ),
    re_path(
        r"events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/pos$",
        tickets_admin_pos_view,
        name="tickets_admin_pos_view",
    ),
]
