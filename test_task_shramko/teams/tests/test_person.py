import copy

from django.urls import reverse
from rest_framework import status

from teams.models import Person
from teams.tests import CustomTestCase


class TestPersonCreate(CustomTestCase):
    URL = reverse("person-list")
    METHOD = "POST"
    VALID_DATA = {"first_name": "Person", "last_name": "C", "email": "person.c@example.com"}
    EXPECTED_STATUS = 201

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.VALID_DATA["teams"] = [cls.team_a.id]

    def test_valid_data(self):
        self.check_status(self.URL, self.METHOD, self.VALID_DATA, self.EXPECTED_STATUS)

    def test_email_already_exists(self):
        data = copy.copy(self.VALID_DATA)
        data.pop("teams")
        person_c = Person.objects.create(**data)
        person_c.teams.set([self.team_a.id])

        response = self.check_status(self.URL, self.METHOD, self.VALID_DATA, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["email"][0].code, "unique")

    def test_no_email(self):
        data = copy.copy(self.VALID_DATA)
        data.pop("email")
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["email"][0].code, "required")

    def test_too_long_email(self):
        data = copy.copy(self.VALID_DATA)
        data["email"] = "a" * 300
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["email"][0].code, "max_length")

    def test_too_long_first_name(self):
        data = copy.copy(self.VALID_DATA)
        data["first_name"] = "a" * 129
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["first_name"][0].code, "max_length")

    def test_too_long_last_name(self):
        data = copy.copy(self.VALID_DATA)
        data["first_name"] = "a" * 129
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["first_name"][0].code, "max_length")

    def test_invalid_team(self):
        data = copy.copy(self.VALID_DATA)
        data["teams"] = ["abc"]
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["teams"][0].code, "incorrect_type")

    def test_not_existing_team(self):
        data = copy.copy(self.VALID_DATA)
        data["teams"] = [100]
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["teams"][0].code, "does_not_exist")


class TestPersonList(CustomTestCase):
    METHOD = "GET"
    URL = reverse("person-list")

    def test_valid(self):
        self.check_status(self.URL, self.METHOD)


class TestPersonRetrieve(CustomTestCase):
    METHOD = "GET"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL = reverse("person-detail", args=[cls.person_b.id])

    def test_valid(self):
        self.check_status(self.URL, self.METHOD)

    def test_invalid_id(self):
        url = reverse("person-detail", args=["abc"])
        self.check_status(url, self.METHOD, expected_status=status.HTTP_404_NOT_FOUND)


class TestPersonUpdate(CustomTestCase):
    METHOD = "PUT"
    VALID_DATA = {"first_name": "Changed Person", "last_name": "Changed C", "email": "changed.person.c@example.com"}

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL = reverse("person-detail", args=[cls.person_b.id])
        cls.VALID_DATA["teams"] = [cls.team_a.id]

    def test_valid_data(self):
        response = self.check_status(self.URL, self.METHOD, self.VALID_DATA)
        self.assertEqual(response["teams"], self.VALID_DATA["teams"])

    def test_email_already_exists(self):
        data = copy.copy(self.VALID_DATA)
        data.pop("teams")
        person_c = Person.objects.create(**data)
        person_c.teams.set([self.team_a.id])

        response = self.check_status(self.URL, self.METHOD, self.VALID_DATA, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["email"][0].code, "unique")

    def test_no_email(self):
        data = copy.copy(self.VALID_DATA)
        data.pop("email")
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["email"][0].code, "required")

    def test_too_long_email(self):
        data = copy.copy(self.VALID_DATA)
        data["email"] = "a" * 300
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["email"][0].code, "max_length")

    def test_too_long_first_name(self):
        data = copy.copy(self.VALID_DATA)
        data["first_name"] = "a" * 129
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["first_name"][0].code, "max_length")

    def test_too_long_last_name(self):
        data = copy.copy(self.VALID_DATA)
        data["first_name"] = "a" * 129
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["first_name"][0].code, "max_length")

    def test_invalid_team(self):
        data = copy.copy(self.VALID_DATA)
        data["teams"] = ["abc"]
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["teams"][0].code, "incorrect_type")

    def test_not_existing_team(self):
        data = copy.copy(self.VALID_DATA)
        data["teams"] = [100]
        response = self.check_status(self.URL, self.METHOD, data, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["teams"][0].code, "does_not_exist")


class TestPersonDestroy(CustomTestCase):
    METHOD = "DELETE"
    EXPECTED_STATUS = 204

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL = reverse("person-detail", args=[cls.person_b.id])

    def test_valid(self):
        self.check_status(self.URL, self.METHOD, expected_status=self.EXPECTED_STATUS)

    def test_invalid_id(self):
        url = reverse("person-detail", args=["abc"])
        self.check_status(url, self.METHOD, expected_status=status.HTTP_404_NOT_FOUND)
