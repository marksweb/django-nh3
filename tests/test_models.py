from django.db import models
from django.test import TestCase
from django.utils.safestring import SafeString
from django_nh3.models import Nh3Field


class Nh3Content(models.Model):
    """Bleach test model"""

    CHOICES = (("f", "first choice"), ("s", "second choice"))
    content = Nh3Field(
        strip_comments=True,
    )
    choice = Nh3Field(choices=CHOICES)
    blank_field = Nh3Field(blank=True)
    null_field = Nh3Field(blank=True, null=True)


class Nh3NullableContent(models.Model):
    """Bleach test model"""

    content = Nh3Field(blank=True, null=True)


class TestNh3ModelField(TestCase):
    """Test model field"""

    def test_cleaning(self):
        """Test values are bleached"""
        test_data = {
            "html_data": "<h1>Heading</h1>",
            "no_html": "Heading",
            "html_comment": "<!-- this is a comment -->",
        }
        expected_values = {
            "html_data": "Heading",
            "no_html": "Heading",
            "html_comment": "",
        }

        for key, value in test_data.items():
            obj = Nh3Content.objects.create(content=value)
            self.assertEqual(obj.content, expected_values[key])

    def test_retrieved_values_are_template_safe(self):
        obj = Nh3Content.objects.create(content="some content")
        obj.refresh_from_db()
        self.assertIsInstance(obj.content, SafeString)
        obj = Nh3Content.objects.create(content="")
        obj.refresh_from_db()
        self.assertIsInstance(obj.content, SafeString)

    def test_saved_values_are_template_safe(self):
        obj = Nh3Content(content="some content")
        obj.save()
        self.assertIsInstance(obj.content, SafeString)
        obj = Nh3Content(content="")
        obj.save()
        self.assertIsInstance(obj.content, SafeString)

    def test_saved_none_values_are_none(self):
        obj = Nh3Content(null_field=None)
        obj.save()
        self.assertIsNone(obj.null_field)


class TestNh3NullableModelField(TestCase):
    """Test model field"""

    def test_cleaning(self):
        """Test values are bleached"""
        test_data = {
            "none": None,
            "empty": "",
            "whitespaces": "   ",
            "linebreak": "\n",
        }
        expected_values = {
            "none": None,
            "empty": "",
            "whitespaces": "   ",
            "linebreak": "\n",
        }

        for key, value in test_data.items():
            obj = Nh3NullableContent.objects.create(content=value)
            self.assertEqual(obj.content, expected_values[key])
