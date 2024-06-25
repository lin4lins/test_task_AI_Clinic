from django.urls import path, include
from rest_framework.routers import DefaultRouter

from teams.views.person import PersonViewSet
from teams.views.team import TeamViewSet

router = DefaultRouter()
router.register(r"teams", TeamViewSet)
router.register(r"people", PersonViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
