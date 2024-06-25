from rest_framework.test import APITestCase

from teams.models import Team, Person
from teams.tests.test_data import TEAM_A, TEAM_B, PERSON_A, PERSON_B


class CustomTestCase(APITestCase):
    URL = None
    METHOD = None
    VALID_DATA = None

    @classmethod
    def setUpTestData(cls):
        cls.team_a = Team.objects.create(**TEAM_A)
        cls.team_b = Team.objects.create(**TEAM_B)
        cls.person_a = Person.objects.create(**PERSON_A)
        cls.person_b = Person.objects.create(**PERSON_B)
        cls.person_b.teams.set([cls.team_a, cls.team_b])

    def check_status(self, url, method, data=None, expected_status=200):
        """
        Checks the status of an HTTP request and asserts the expected status code.

        Args:
            url (str): The URL to which the request is made.
            method (str): The HTTP method to use (e.g., 'get', 'post', 'put', 'delete').
            data (dict, optional): The data to send with the request. Defaults to None.
            expected_status (int, optional): The expected HTTP status code. Defaults to 200.

        Returns:
            dict: The response data from the HTTP request.

        Raises:
            AssertionError: If the actual status code does not match the expected status code.
        """
        chosen_http_method = getattr(self.client, method.lower())
        response = chosen_http_method(url, data, format="json") if data else chosen_http_method(url)

        failure_message = (
            f"{method} method access test failed. " f"Expected {expected_status}, got {response.status_code}."
        )

        self.assertEqual(response.status_code, expected_status, failure_message)

        return response.data
