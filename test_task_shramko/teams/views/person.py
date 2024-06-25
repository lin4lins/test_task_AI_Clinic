from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from teams.models import Person
from teams.serializers import PersonSerializer, TeamSerializer


@extend_schema(tags=["People"])
class PersonViewSet(viewsets.ModelViewSet):
    """
    Class representing the view set for managing people.

    This view set provides CRUD operations for the Person model.
    """

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = "id"

    @action(detail=True, methods=["get"])
    def teams(self, request, id=None):
        person = self.get_object()
        teams = person.teams.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
