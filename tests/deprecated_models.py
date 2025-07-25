from django.db import models

from django_nh3.models import Nh3Field


class Nh3FieldContent(models.Model):
    """NH3 test model"""

    content = Nh3Field()
