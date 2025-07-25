from unittest.mock import patch

from django.test import TestCase

from django_nh3.utils import get_nh3_default_options, normalize_nh3_options

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


def set_test_flag_true():
    return "set_test_flag_true"


class TestNormalizeNh3Options(TestCase):
    def test_unrecognized_keys_are_passed_through(self):
        self.assertEqual(normalize_nh3_options({"unknown": None}), {"unknown": None})
        self.assertEqual(normalize_nh3_options({"unknown": []}), {"unknown": []})
        self.assertEqual(normalize_nh3_options({"unknown": ()}), {"unknown": ()})
        self.assertEqual(normalize_nh3_options({"unknown": set()}), {"unknown": set()})

    def test_tags_clean_content_tags_generic_attribute_prefixes_and_url_schemes(self):
        for kwargs, expected in [
            (
                {"tags": ["one", "two", "three"]},
                {"tags": {"one", "two", "three"}},
            ),
            (
                {"clean_content_tags": ["two", "three", "four"]},
                {"clean_content_tags": {"two", "three", "four"}},
            ),
            (
                {"generic_attribute_prefixes": ["three", "four", "five"]},
                {"generic_attribute_prefixes": {"three", "four", "five"}},
            ),
            (
                {"url_schemes": ["four", "five", "six"]},
                {"url_schemes": {"four", "five", "six"}},
            ),
        ]:
            with self.subTest(kwargs=kwargs, expected=expected):
                self.assertDictEqual(
                    normalize_nh3_options(kwargs),
                    expected,
                )

    def test_attribute_filter(self):
        self.assertDictEqual(
            normalize_nh3_options({"attribute_filter": set_test_flag_true}),
            {"attribute_filter": set_test_flag_true},
        )

        # Make sure that the function is exactly what we expect
        result = normalize_nh3_options({"attribute_filter": set_test_flag_true})
        self.assertEqual(result["attribute_filter"](), "set_test_flag_true")

        self.assertDictEqual(
            normalize_nh3_options(
                {"attribute_filter": "tests.test_settings.set_test_flag_true"}
            ),
            {"attribute_filter": set_test_flag_true},
        )

        # Make sure that the function is exactly what we expect
        result = normalize_nh3_options({"attribute_filter": set_test_flag_true})
        self.assertEqual(result["attribute_filter"](), "set_test_flag_true")

    def test_strip_comments(self):
        for kwargs, expected in [
            (
                {"strip_comments": None},
                {"strip_comments": False},
            ),
            (
                {"strip_comments": []},
                {"strip_comments": False},
            ),
            (
                {"strip_comments": ""},
                {"strip_comments": False},
            ),
            (
                {"strip_comments": True},
                {"strip_comments": True},
            ),
            (
                {"strip_comments": "happy"},
                {"strip_comments": True},
            ),
        ]:
            with self.subTest(kwargs=kwargs, expected=expected):
                self.assertDictEqual(
                    normalize_nh3_options(kwargs),  # type: ignore[arg-type]
                    expected,
                )

    def test_link_rel(self):
        for kwargs, expected in [
            (
                {"link_rel": ""},
                {"link_rel": ""},
            ),
            (
                {"link_rel": "my string"},
                {"link_rel": "my string"},
            ),
            (
                {"link_rel": 0},
                {"link_rel": "0"},
            ),
            (
                {"link_rel": None},
                {"link_rel": "None"},
            ),
            (
                {"link_rel": True},
                {"link_rel": "True"},
            ),
            (
                {"link_rel": False},
                {"link_rel": "False"},
            ),
        ]:
            with self.subTest(kwargs=kwargs, expected=expected):
                self.assertDictEqual(
                    normalize_nh3_options(kwargs),  # type: ignore[arg-type]
                    expected,
                )

    def assertDataStructureEqual(self, left, right):
        if isinstance(left, set):
            self.assertIsInstance(right, set)
            self.assertSetEqual(left, right)
        elif isinstance(left, dict):
            self.assertIsInstance(right, dict)
            self.assertEqual(left.keys(), right.keys())
            for key in left.keys():
                self.assertIn(key, right.keys())
                self.assertDataStructureEqual(left[key], right[key])
        else:
            self.assertIsInstance(right, left.__class__)
            self.assertEqual(left, right)

    def test_tag_attribute_values(self):
        self.assertDataStructureEqual(
            normalize_nh3_options(
                {
                    "tag_attribute_values": {
                        "tag1": {
                            "attrA": ["A1", "A2", "A3"],
                            "attrB": ("B1", "B2", "B3"),
                        },
                        "tag2": {
                            "attrC": ["C1", "C2", "C3"],
                        },
                    },
                }
            ),
            {
                "tag_attribute_values": {
                    "tag1": {
                        "attrA": {"A1", "A2", "A3"},
                        "attrB": {"B1", "B2", "B3"},
                    },
                    "tag2": {
                        "attrC": {"C1", "C2", "C3"},
                    },
                },
            },
        )

    def test_set_tag_attribute_values(self):
        self.assertDataStructureEqual(
            normalize_nh3_options(
                {
                    "set_tag_attribute_values": {
                        "tag1": {
                            "attrA": "Avalue",
                            "attrB": "Bvalue",
                        },
                        "tag2": {
                            "attrC": "Cvalue",
                        },
                    },
                }
            ),
            {
                "set_tag_attribute_values": {
                    "tag1": {
                        "attrA": "Avalue",
                        "attrB": "Bvalue",
                    },
                    "tag2": {
                        "attrC": "Cvalue",
                    },
                },
            },
        )
