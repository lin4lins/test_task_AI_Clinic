from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from teams.models import Team
from teams.serializers import TeamSerializer, PersonSerializer


@extend_schema(tags=["Teams"])
class TeamViewSet(viewsets.ModelViewSet):
    """
    Class representing the view set for managing teams.

    This view set provides CRUD operations for the Team model.
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = "id"

    @action(detail=True, methods=["get"])
    def people(self, request, id=None):
        team = self.get_object()
        people = team.people.all()
        serializer = PersonSerializer(people, many=True)
        return Response(serializer.data)
