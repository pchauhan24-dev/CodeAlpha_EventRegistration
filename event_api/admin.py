
from django.contrib import admin
from .models import Event, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "date",
        "location",
        "capacity",
        "created_at",
    )
    search_fields = ("name", "location")
    list_filter = ("date", "location")
    ordering = ("date",)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "attendee_name",
        "attendee_email",
        "event",
        "registered_at",
    )
    search_fields = (
        "attendee_name",
        "attendee_email",
        "event__name",
    )
    list_filter = ("event", "registered_at")
    ordering = ("-registered_at",)
