from django.test import override_settings

from django_nh3.checks import check_nh3_settings


@override_settings(NH3_ALLOWED_ATTRIBUTES={"div": {"style"}})
def test_check_warns_about_style():
    errors = check_nh3_settings(None)
    assert len(errors) == 1
    assert errors[0].id == "django_nh3.W001"


@override_settings(NH3_ALLOWED_ATTRIBUTES={"div": {"class", "id"}})
def test_check_is_silent_when_safe():
    errors = check_nh3_settings(None)
    assert len(errors) == 0


@override_settings(NH3_ALLOWED_ATTRIBUTES={})
def test_check_handles_empty_dict():
    errors = check_nh3_settings(None)
    assert len(errors) == 0


@override_settings(NH3_ALLOWED_ATTRIBUTES=None)
def test_check_handles_non_dict_attributes():
    errors = check_nh3_settings(None)
    assert len(errors) == 0