from django.db import models
from django.forms import ModelForm
from django.test import TestCase
from django.utils.safestring import SafeString

from django_nh3.models import Nh3Text


class Nh3Content(models.Model):
    """NH3 test model"""

    content = Nh3Text(
        strip_comments=True,
    )
    blank_field = Nh3Text(blank=True)
    null_field = Nh3Text(blank=True, null=True)


class Nh3ContentModelForm(ModelForm):
    """NH3 test model form"""

    class Meta:
        model = Nh3Content
        fields = ["content"]


class Nh3NullableContent(models.Model):
    """NH3 test model"""

    CHOICES = (("f", "first choice"), ("s", "second choice"))
    choice = Nh3Text(choices=CHOICES, blank=True)
    content = Nh3Text(blank=True, null=True)


class Nh3NullableContentModelForm(ModelForm):
    """NH3 test model form"""

    class Meta:
        model = Nh3NullableContent
        fields = ["choice"]


class TestNh3ModelField(TestCase):
    """Test model field"""

    def test_cleaning(self):
        """Test values are sanitized"""
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
        """Test values are sanitized"""
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


class TestNh3ModelFormField(TestCase):
    """Test model form field"""

    def test_cleaning(self):
        """Test values are sanitized"""
        test_data = {
            "html_data": "<h1>Heading</h1>",
            "no_html": "Heading",
            "spacing": " Heading ",
        }
        expected_values = {
            "html_data": "Heading",
            "no_html": "Heading",
            "spacing": "Heading",
        }

        for key, value in test_data.items():
            form = Nh3ContentModelForm(data={"content": value})
            self.assertTrue(form.is_valid())
            obj = form.save()
            self.assertEqual(obj.content, expected_values[key])

    def test_stripped_comments(self):
        """Content field strips comments so ensure they aren't allowed"""

        self.assertFalse(
            Nh3ContentModelForm(
                data={"content": "<!-- this is a comment -->"}
            ).is_valid()
        )

    def test_field_choices(self):
        """Content field strips comments so ensure they aren't allowed"""
        test_data = dict(Nh3NullableContent.CHOICES)

        for key, value in test_data.items():
            form = Nh3NullableContentModelForm(data={"choice": key})
            self.assertTrue(form.is_valid())
            obj = form.save()
            self.assertEqual(obj.get_choice_display(), value)
