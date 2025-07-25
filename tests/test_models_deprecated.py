from django.test import TestCase


class TestNh3FieldModelField(TestCase):
    """Test deprecated model field"""

    def test_init_raises_warning(self):
        with self.assertWarns(DeprecationWarning):
            from .deprecated_models import Nh3FieldContent  # noqa: F401
