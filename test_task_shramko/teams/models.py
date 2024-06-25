from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    teams = models.ManyToManyField(Team, related_name="people")
