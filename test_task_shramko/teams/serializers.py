from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from teams.models import Person, Team
from teams.schema_constants import (
    EMAIL_EXAMPLE,
    FIRST_NAME_EXAMPLE,
    ID_EXAMPLE,
    LAST_NAME_EXAMPLE,
    TEAM_NAME_EXAMPLE,
    TEAMS_EXAMPLE,
)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Team",
            value={
                "name": TEAM_NAME_EXAMPLE,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Team",
            value={
                "id": ID_EXAMPLE,
                "name": TEAM_NAME_EXAMPLE,
            },
            response_only=True,
        ),
    ]
)
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Person",
            value={
                "first_name": FIRST_NAME_EXAMPLE,
                "last_name": LAST_NAME_EXAMPLE,
                "email": EMAIL_EXAMPLE,
                "teams": TEAMS_EXAMPLE,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Person",
            value={
                "id": ID_EXAMPLE,
                "first_name": FIRST_NAME_EXAMPLE,
                "last_name": LAST_NAME_EXAMPLE,
                "email": EMAIL_EXAMPLE,
                "teams": TEAMS_EXAMPLE,
            },
            response_only=True,
        ),
    ]
)
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"
