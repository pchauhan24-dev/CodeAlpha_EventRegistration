
from rest_framework import serializers
from .models import Event, Registration


class EventSerializer(serializers.ModelSerializer):
    registered_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "date",
            "location",
            "capacity",
            "registered_count",
            "created_at",
        ]
        read_only_fields = ["id", "registered_count", "created_at"]

    def get_registered_count(self, obj):
        return obj.registrations.count()

    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Event capacity must be at least 1."
            )
        return value


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            "id",
            "event",
            "attendee_name",
            "attendee_email",
            "registered_at",
        ]
        read_only_fields = ["id", "registered_at"]

    def validate(self, attrs):
        event = attrs.get("event")
        email = attrs.get("attendee_email", "").strip().lower()

        if event:
            if event.registrations.count() >= event.capacity:
                raise serializers.ValidationError(
                    "This event has reached its maximum capacity."
                )

            if event.registrations.filter(
                attendee_email__iexact=email
            ).exists():
                raise serializers.ValidationError(
                    "This email is already registered for this event."
                )

        attrs["attendee_email"] = email
        return attrs
