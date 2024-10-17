from django.test import TestCase
from django.utils.safestring import SafeString

from django_nh3.forms import Nh3Field

# import urls to get coverage
from . import urls  # noqa: F401


class TestNh3Field(TestCase):
    def test_empty(self):
        """
        Test that the empty_value arg is returned for any input empty value
        """
        for requested_empty_value in ("", None):
            field = Nh3Field(empty_value=requested_empty_value)
            for empty_value in field.empty_values:
                self.assertEqual(field.to_python(empty_value), requested_empty_value)

    def test_return_type(self):
        """Test bleached values are SafeString objects"""
        field = Nh3Field()
        self.assertIsInstance(field.to_python("some text"), str)
        self.assertIsInstance(field.to_python("<h1>some text</h1>"), SafeString)

    def test_values(self):
        """Test bleached values are SafeString objects"""
        field = Nh3Field()
        self.assertEqual(field.to_python("some text"), "some text")
        self.assertEqual(field.to_python(" some text "), "some text")
        self.assertEqual(field.to_python("<h1>some text</h1>"), "some text")
