from unittest.mock import patch

from django.test import TestCase
from django_nh3.utils import get_nh3_default_options

from .constants import ALLOWED_ATTRIBUTES, ALLOWED_TAGS, STRIP_COMMENTS


class TestBleachOptions(TestCase):
    @patch(
        "django_nh3.utils.settings",
        NH3_ALLOWED_ATTRIBUTES=ALLOWED_ATTRIBUTES,
    )
    def test_custom_attrs(self, settings):
        nh3_args = get_nh3_default_options()
        self.assertEqual(nh3_args["attributes"], ALLOWED_ATTRIBUTES)

    @patch(
        "django_nh3.utils.settings",
        NH3_ALLOWED_TAGS=ALLOWED_TAGS,
    )
    def test_custom_tags(self, settings):
        nh3_args = get_nh3_default_options()
        self.assertEqual(nh3_args["tags"], ALLOWED_TAGS)

    @patch(
        "django_nh3.utils.settings",
        NH3_STRIP_COMMENTS=STRIP_COMMENTS,
    )
    def test_strip_comments(self, settings):
        nh3_args = get_nh3_default_options()
        self.assertEqual(nh3_args["strip_comments"], STRIP_COMMENTS)
