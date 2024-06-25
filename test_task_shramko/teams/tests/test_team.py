import copy

from django.urls import reverse
from rest_framework import status

from teams.models import Team
from teams.tests import CustomTestCase


class TestTeamCreate(CustomTestCase):
    URL = reverse("team-list")
    METHOD = "POST"
    VALID_DATA = {"name": "Team C"}
    EXPECTED_STATUS = 201

    def test_valid_data(self):
        self.check_status(self.URL, self.METHOD, self.VALID_DATA, self.EXPECTED_STATUS)

    def test_name_already_exists(self):
        Team.objects.create(**self.VALID_DATA)
        response = self.check_status(self.URL, self.METHOD, self.VALID_DATA, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["name"][0].code, "unique")

    def test_no_name(self):
        data = copy.copy(self.VALID_DATA)
        data.pop("name")
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["name"][0].code, "required")

    def test_too_long_name(self):
        data = copy.copy(self.VALID_DATA)
        data["name"] = "a" * 129
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["name"][0].code, "max_length")


class TestTeamList(CustomTestCase):
    METHOD = "GET"
    URL = reverse("team-list")

    def test_valid(self):
        self.check_status(self.URL, self.METHOD)


class TestTeamRetrieve(CustomTestCase):
    METHOD = "GET"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL = reverse("team-detail", args=[cls.team_b.id])

    def test_valid(self):
        self.check_status(self.URL, self.METHOD)

    def test_invalid_id(self):
        url = reverse("team-detail", args=["abc"])
        self.check_status(url, self.METHOD, expected_status=status.HTTP_404_NOT_FOUND)


class TestTeamUpdate(CustomTestCase):
    METHOD = "PUT"
    VALID_DATA = {"name": "Changed name"}

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL = reverse("team-detail", args=[cls.team_b.id])

    def test_valid(self):
        response = self.check_status(self.URL, self.METHOD, self.VALID_DATA)
        self.assertEqual(response["name"], self.VALID_DATA["name"])

    def test_invalid_id(self):
        url = reverse("team-detail", args=["abc"])
        self.check_status(url, self.METHOD, expected_status=status.HTTP_404_NOT_FOUND)

    def test_name_already_exists(self):
        Team.objects.create(**self.VALID_DATA)
        response = self.check_status(self.URL, self.METHOD, self.VALID_DATA, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["name"][0].code, "unique")

    def test_no_name(self):
        data = copy.copy(self.VALID_DATA)
        data.pop("name")
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["name"][0].code, "required")

    def test_too_long_name(self):
        data = copy.copy(self.VALID_DATA)
        data["name"] = "a" * 129
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["name"][0].code, "max_length")


class TestTeamPartialUpdate(CustomTestCase):
    METHOD = "PATCH"
    VALID_DATA = {"name": "Changed name"}

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL = reverse("team-detail", args=[cls.team_b.id])

    def test_valid(self):
        response = self.check_status(self.URL, self.METHOD, self.VALID_DATA)
        self.assertEqual(response["name"], self.VALID_DATA["name"])

    def test_invalid_id(self):
        url = reverse("team-detail", args=["abc"])
        self.check_status(url, self.METHOD, expected_status=status.HTTP_404_NOT_FOUND)

    def test_name_already_exists(self):
        Team.objects.create(**self.VALID_DATA)
        response = self.check_status(self.URL, self.METHOD, self.VALID_DATA, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["name"][0].code, "unique")

    def test_too_long_name(self):
        data = copy.copy(self.VALID_DATA)
        data["name"] = "a" * 129
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["name"][0].code, "max_length")


class TestTeamDestroy(CustomTestCase):
    METHOD = "DELETE"
    EXPECTED_STATUS = 204

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL = reverse("team-detail", args=[cls.team_b.id])

    def test_valid(self):
        self.check_status(self.URL, self.METHOD, expected_status=self.EXPECTED_STATUS)

    def test_invalid_id(self):
        url = reverse("team-detail", args=["abc"])
        self.check_status(url, self.METHOD, expected_status=status.HTTP_404_NOT_FOUND)


class TestTeamPeopleRetrieve(CustomTestCase):
    METHOD = "GET"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL = reverse("team-people", args=[cls.team_b.id])

    def test_valid(self):
        self.check_status(self.URL, self.METHOD)

    def test_invalid_id(self):
        url = reverse("team-detail", args=["abc"])
        self.check_status(url, self.METHOD, expected_status=status.HTTP_404_NOT_FOUND)
