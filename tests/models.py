from django.db import models

from django_nh3.models import Nh3CharField, Nh3TextField


class Nh3CharFieldContent(models.Model):
    """NH3 test model"""

    content = Nh3CharField(
        strip_comments=True,
        max_length=1000,
    )
    blank_field = Nh3CharField(blank=True, max_length=1000)
    null_field = Nh3CharField(blank=True, null=True, max_length=1000)


class Nh3CharFieldNullableContent(models.Model):
    """NH3 test model"""

    CHOICES = (("f", "first choice"), ("s", "second choice"))
    choice = Nh3CharField(choices=CHOICES, blank=True, max_length=1000)
    content = Nh3CharField(blank=True, null=True, max_length=1000)


class Nh3TextFieldContent(models.Model):
    """NH3 test model"""

    content = Nh3TextField(
        strip_comments=True,
        max_length=1000,
    )
    blank_field = Nh3TextField(blank=True, max_length=1000)
    null_field = Nh3TextField(blank=True, null=True, max_length=1000)


class Nh3TextFieldNullableContent(models.Model):
    """NH3 test model"""

    CHOICES = (("f", "first choice"), ("s", "second choice"))
    choice = Nh3TextField(choices=CHOICES, blank=True, max_length=1000)
    content = Nh3TextField(blank=True, null=True, max_length=1000)
