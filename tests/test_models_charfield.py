from django.test import TestCase
from django.utils.safestring import SafeString

from .forms import Nh3CharFieldContentModelForm, Nh3CharFieldNullableContentModelForm
from .models import Nh3CharFieldContent, Nh3CharFieldNullableContent


class TestNh3ModelCharField(TestCase):
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
            obj = Nh3CharFieldContent.objects.create(content=value)
            self.assertEqual(obj.content, expected_values[key])

    def test_retrieved_values_are_template_safe(self):
        obj = Nh3CharFieldContent.objects.create(content="some content")
        obj.refresh_from_db()
        self.assertIsInstance(obj.content, SafeString)
        obj = Nh3CharFieldContent.objects.create(content="")
        obj.refresh_from_db()
        self.assertIsInstance(obj.content, SafeString)

    def test_saved_values_are_template_safe(self):
        obj = Nh3CharFieldContent(content="some content")
        obj.save()
        self.assertIsInstance(obj.content, SafeString)
        obj = Nh3CharFieldContent(content="")
        obj.save()
        self.assertIsInstance(obj.content, SafeString)

    def test_saved_none_values_are_none(self):
        obj = Nh3CharFieldContent(null_field=None)
        obj.save()
        self.assertIsNone(obj.null_field)


class TestNh3CharFieldNullableModelField(TestCase):
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
            obj = Nh3CharFieldNullableContent.objects.create(content=value)
            self.assertEqual(obj.content, expected_values[key])


class TestNh3CharFieldModelFormField(TestCase):
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
            form = Nh3CharFieldContentModelForm(data={"content": value})
            self.assertTrue(form.is_valid())
            obj = form.save()
            self.assertEqual(obj.content, expected_values[key])

    def test_stripped_comments(self):
        """Content field strips comments so ensure they aren't allowed"""

        self.assertFalse(
            Nh3CharFieldContentModelForm(
                data={"content": "<!-- this is a comment -->"}
            ).is_valid()
        )

    def test_field_choices(self):
        """Content field strips comments so ensure they aren't allowed"""
        test_data = dict(Nh3CharFieldNullableContent.CHOICES)

        for key, value in test_data.items():
            form = Nh3CharFieldNullableContentModelForm(data={"choice": key})
            self.assertTrue(form.is_valid())
            obj = form.save()
            self.assertEqual(obj.get_choice_display(), value)
