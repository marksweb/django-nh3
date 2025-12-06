from typing import Any

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import CheckMessage, Tags, Warning, register


@register(Tags.security)
def check_nh3_settings(
    app_configs: list[AppConfig] | None, **kwargs: Any
) -> list[CheckMessage]:
    """
    Inspects the NH3_ALLOWED_ATTRIBUTES setting to ensure that the 'style'
    attribute is not allowed, as nh3 does not sanitize CSS content.
    """
    errors: list[CheckMessage] = []
    allowed_attributes = getattr(settings, "NH3_ALLOWED_ATTRIBUTES", {})

    found_style = False
    if isinstance(allowed_attributes, dict):
        for _tag, attrs in allowed_attributes.items():
            if "style" in attrs:
                found_style = True
                break

    if found_style:
        errors.append(
            Warning(
                "The 'style' attribute is allowed in NH3_ALLOWED_ATTRIBUTES.",
                hint=(
                    "Allowing 'style' poses a security risk (XSS) because nh3 "
                    "does not sanitize CSS content. Ensure you strictly trust "
                    "the input if this attribute is required."
                ),
                id="django_nh3.W001",
            )
        )
    return errors